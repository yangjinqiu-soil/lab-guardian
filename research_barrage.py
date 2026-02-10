import sys
import time
import threading
import random
from dataclasses import dataclass

from pynput import keyboard, mouse

from PySide6.QtCore import Qt, QTimer, QPoint, QRect
from PySide6.QtGui import QFont, QGuiApplication
from PySide6.QtWidgets import QApplication, QWidget, QLabel

import win32gui
import win32process
import psutil


@dataclass
class Settings:
    idle_seconds: int = 300
    show_seconds: int = 8
    cooldown_seconds: int = 120
    check_interval_ms: int = 1000
    tiny_move_threshold_px: int = 3

    messages: tuple = (
        "下周开组会",
        "再写一句求求了",
        "再不写怎么毕业",
        "打开word",
        "写一行也是写",
    )


SETTINGS = Settings()


def get_foreground_app_title():
    try:
        hwnd = win32gui.GetForegroundWindow()
        title = win32gui.GetWindowText(hwnd) or ""
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        proc = psutil.Process(pid)
        return (proc.name(), title)
    except Exception:
        return ("", "")


class BarrageWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.Tool
        )
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)

        font = QFont("Microsoft YaHei", 18)
        font.setBold(True)
        self.label.setFont(font)

        self.label.setStyleSheet("""
            QLabel {
                color: white;
                background-color: rgba(0, 0, 0, 170);
                padding: 14px 22px;
                border-radius: 18px;
            }
        """)

        self._hide_timer = QTimer(self)
        self._hide_timer.setSingleShot(True)
        self._hide_timer.timeout.connect(self.hide)

    def show_message(self, text: str, duration_s: int = 8):
        self.label.setText(text)
        self.label.adjustSize()

        from PySide6.QtGui import QCursor
        screen = QGuiApplication.screenAt(QCursor.pos()) or QGuiApplication.primaryScreen()
        geo: QRect = screen.availableGeometry()

        x = geo.x() + (geo.width() - self.label.width()) // 2
        y = geo.y() + int(geo.height() * 0.18)

        self.setGeometry(x, y, self.label.width(), self.label.height())
        self.show()
        self.raise_()
        self.activateWindow()

        self._hide_timer.start(duration_s * 1000)


class ActivityMonitor:
    def __init__(self):
        self._lock = threading.Lock()
        self.last_activity = time.time()
        self.last_barrage = 0.0
        self._last_mouse_pos = None

        self._kb_listener = keyboard.Listener(on_press=self._on_key)
        self._ms_listener = mouse.Listener(on_move=self._on_move, on_click=self._on_click, on_scroll=self._on_scroll)

    def start(self):
        self._kb_listener.start()
        self._ms_listener.start()

    def stop(self):
        self._kb_listener.stop()
        self._ms_listener.stop()

    def mark_activity(self):
        with self._lock:
            self.last_activity = time.time()

    def _on_key(self, key):
        self.mark_activity()

    def _on_click(self, x, y, button, pressed):
        self.mark_activity()

    def _on_scroll(self, x, y, dx, dy):
        self.mark_activity()

    def _on_move(self, x, y):
        with self._lock:
            if self._last_mouse_pos is None:
                self._last_mouse_pos = (x, y)
                self.last_activity = time.time()
                return

            lx, ly = self._last_mouse_pos
            if abs(x - lx) + abs(y - ly) >= SETTINGS.tiny_move_threshold_px:
                self._last_mouse_pos = (x, y)
                self.last_activity = time.time()

    def should_trigger_barrage(self) -> bool:
        now = time.time()
        with self._lock:
            idle = now - self.last_activity
            if idle < SETTINGS.idle_seconds:
                return False
            if now - self.last_barrage < SETTINGS.cooldown_seconds:
                return False
            self.last_barrage = now
            return True

    def pick_message(self) -> str:
        return random.choice(SETTINGS.messages)


def main():
    app = QApplication(sys.argv)
    barrage = BarrageWindow()
    monitor = ActivityMonitor()
    monitor.start()

    timer = QTimer()
    timer.setInterval(SETTINGS.check_interval_ms)

    def tick():
        if monitor.should_trigger_barrage():
            msg = monitor.pick_message()
            barrage.show_message(msg, SETTINGS.show_seconds)

    timer.timeout.connect(tick)
    timer.start()

    exit_code = app.exec()
    monitor.stop()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
