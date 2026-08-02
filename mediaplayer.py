#!/usr/bin/env python3

# Waybar mediaplayer module - shows currently playing track via MPRIS/D-Bus.
# Usage:
#   mediaplayer.py                        (auto-detect any running player)
#   mediaplayer.py --player <name>        (filter to a specific player)

import argparse
import subprocess
import sys
import json


def print_output(text, player, class_name):
    if player.startswith("spotify"):
        icon = "\uf1bc"
    else:
        icon = "\uf001"
    out = {
        "text": f"{icon} {text}",
        "class": class_name,
        "tooltip": f"Now Playing: {text}",
    }
    sys.stdout.write(f" {json.dumps(out)}\n")
    sys.stdout.flush()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--player", default="")
    args = parser.parse_args()

    filter = args.player if args.player else "audacious,clementine,mpd,spotify,vlc"

    try:
        result = subprocess.run(
            [
                "playerctl",
                "metadata",
                "--format",
                "{{artist}} - {{title}}",
                "-p",
                filter,
            ],
            capture_output=True,
            text=True,
            timeout=5,
        )
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("")
        return

    if result.returncode != 0:
        print("")
        return

    text = result.stdout.strip()

    try:
        status_result = subprocess.run(
            ["playerctl", "status", "-p", filter],
            capture_output=True,
            text=True,
            timeout=5,
        )
        status = status_result.stdout.strip() if status_result.returncode == 0 else "Playing"
    except (subprocess.TimeoutExpired, FileNotFoundError):
        status = "Playing"

    print(text, status)


if __name__ == "__main__":
    main()