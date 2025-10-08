#!/usr/bin/env python3
# hypnotic_spiral_circle.py — full circular spiral filling terminal edges
# Usage: python3 hypnotic_spiral_circle.py

import math
import time
import shutil
import sys

# Spiral settings
chars = " .:-=+*#%@"
turns = 30             # more revolutions for depth
points_per_turn = 600  # smoother spiral
phase_speed = -0.05    # counter-clockwise
frame_delay = 0.03
vertical_squash = 0.55  # adjust for terminal font aspect ratio

def clear_screen():
    sys.stdout.write("\033[2J\033[H")
    sys.stdout.flush()

def draw_spiral_frame(phase):
    # Terminal size per frame
    size = shutil.get_terminal_size(fallback=(120, 50))
    width, height = size.columns, size.lines
    cx, cy = width // 2, height // 2

    # True circular max radius
    max_radius = min(cx, int(cy / vertical_squash)) - 1

    total_points = turns * points_per_turn
    screen = [[" "]*width for _ in range(height)]

    for i in range(total_points):
        t = i / total_points  # normalized distance from center
        angle = 2 * math.pi * (i / points_per_turn) + phase
        radius = t * max_radius

        x = cx + radius * math.cos(angle)
        y = cy + radius * math.sin(angle) * vertical_squash
        sx, sy = int(round(x)), int(round(y))

        if 0 <= sx < width and 0 <= sy < height:
            # taper ASCII toward edges
            depth_factor = 1 - t
            char_idx = int(depth_factor * (len(chars)-1))
            ch = chars[char_idx]

            # optional color gradient
            color = 16 + int(t * 215)
            screen[sy][sx] = f"\033[38;5;{color}m{ch}\033[0m"

    sys.stdout.write("\033[H")
    for row in screen:
        sys.stdout.write("".join(row) + "\n")
    sys.stdout.flush()

def main():
    clear_screen()
    phase = 0.0
    try:
        while True:
            draw_spiral_frame(phase)
            phase += phase_speed
            time.sleep(frame_delay)
    except KeyboardInterrupt:
        sys.stdout.write("\033[0m\n")
        sys.exit()

if __name__ == "__main__":
    main()
