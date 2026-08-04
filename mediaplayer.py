#!/usr/bin/env python3

# Waybar mediaplayer module - shows currently playing track via MPRIS/D-Bus.
# Usage:
#   mediaplayer.py                        (auto-detect any running player)
#   mediaplayer.py --player <name>        (filter to a specific player)

import argparse
import subprocess
import sys
import json


def print_output(text, status):
    class_name = status.lower() if status else ""
    if status == "Playing":
        class_name = "playing"
    elif status == "Paused":
        class_name = "paused"

    if text:
        out = {
            "text": f"\uf001\u2002\u2002{text}",
            "class": class_name,
            "tooltip": f"Now Playing: {text}",
        }
        sys.stdout.write(json.dumps(out) + "\n")
    else:
        sys.stdout.write("\n")
    sys.stdout.flush()


player = ""


def main():
    global player
    parser = argparse.ArgumentParser()
    parser.add_argument("--player", default="")
    parser.add_argument("--command", default="",
                        help="not used, kept for compatibility")
    args = parser.parse_args()

    game = args.player
    pick = ["-p", game] if game else []
    player = subprocess.run(
        ["playerctl", "-l"], capture_output=True, text=True, timeout=5
    ).stdout.strip()

    try:
        result = subprocess.run(
            ["playerctl", "metadata", "--format",
                "{{artist}} - {{title}}"] + pick,
            capture_output=True,
            text=True,
            timeout=5,
        )
    except (subprocess.TimeoutExpired, FileNotFoundError):
        sys.stdout.write("\n")
        sys.stdout.flush()
        return

    if result.returncode != 0:
        print_output("", "")
        return

    text = result.stdout.strip()

    try:
        status_result = subprocess.run(
            ["playerctl", "status"] + pick,
            capture_output=True,
            text=True,
            timeout=5,
        )
        status = status_result.stdout.strip() if status_result.returncode == 0 else ""
    except (subprocess.TimeoutExpired, FileNotFoundError):
        status = ""

    print_output(text, status)


if __name__ == "__main__":
    main()
