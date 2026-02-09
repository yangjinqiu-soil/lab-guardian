# Lab Guardian

A lightweight desktop agent that tracks user activity and gently reminds you to refocus when research work pauses.

Lab Guardian helps researchers who spend long hours writing, reading, or analyzing data.
Unlike a timer, it monitors *behavioral inactivity*: if no keyboard or mouse input occurs for a set time, a small transparent overlay appears to encourage you to resume work.

It runs entirely locally and never records screen content, captures screenshots, or uploads data.
The goal is simple—offer timely, nonintrusive feedback that helps maintain steady research momentum without invading privacy.


## Why this exists

Researchers rarely stop working because time expired.
They stop because attention drifts.

Typical workflow interruptions:

* opening a browser “just for one search”
* checking messages
* passive scrolling
* fatigue micro-breaks that turn into long breaks

Lab Guardian detects *behavioral disengagement* rather than elapsed time and acts as a soft intervention tool.

This project explores a simple idea:

> Small, timely behavioral feedback can improve research consistency more than strict schedules.


## Features (current)

* Global keyboard and mouse activity monitoring
* Idle detection (default: 5 minutes)
* Always-on-top translucent overlay notification
* Cooldown to avoid spam reminders
* Fully local execution (no network communication)
* No screen capture or content inspection


## Planned features

* Foreground application classification (writing / reading / analysis / non-research)
* Different prompts depending on context
* Daily research activity statistics
* Focus session tracking
* Custom reminder messages
* Whitelist / blacklist applications
* Optional sound cues


## Privacy

Lab Guardian **does NOT**:

* capture screenshots
* log typed text
* read document content
* send data anywhere

It only checks:

* whether keyboard/mouse activity occurred
* the name/title of the active application window (optional future feature)

All processing is local.

# Project Structure

src/
  monitor/     input activity detection
  context/     active window classification (future)
  ui/          overlay notification
  rules/       classification rules

config/
  rules.json


# Intended Use

This tool is not meant to enforce work or monitor others.

It is a self-regulation aid for individual researchers.


#Contributing

Ideas, feature suggestions, and improvements are welcome.
This project is intentionally small and experimental.


