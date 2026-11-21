#!/usr/bin/env bash
set -euo pipefail

# Headed (stealth) mode needs a display: start Xvfb + a window manager.
rm -f /tmp/.X99-lock /tmp/.X11-unix/X99
setsid Xvfb :99 -screen 0 1920x1080x24 -nolisten tcp &
export DISPLAY=:99
setsid openbox &

exec python /server.py
