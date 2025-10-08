#!/usr/bin/env python3
# golden_spiral_terminal_animated2.py — full-size circular "golden spiral" in terminal

import math
import time
import shutil
import sys

chars = " .:-=+*#%@"
points_per_turn = 200
turns = 20
phase_speed = -0.05
frame_delay = 0.03
vertical_squash = 0.55
phi = 1.61803398875

def clear_screen():
    sys.stdout.write("\033[2J\033[H")
    sys.stdout.flush()

def draw_spiral_frame(phase):
    size = shutil.get_terminal_size(fallback=(120,50))
    width, height = size.columns, size.lines
    cx, cy = width//2, height//2
    max_radius = min(cx, int(cy/vertical_squash)) - 1

    screen = [[" "]*width for _ in range(height)]

    total_points = turns * points_per_turn

    for i in range(total_points):
        t = i / total_points  # 0=center, 1=edge
        # Golden spiral angle: slightly accelerated to mimic phi growth
        angle = 2 * math.pi * i / points_per_turn * phi + phase
        radius = t * max_radius

        x = cx + radius * math.cos(angle)
        y = cy + radius * math.sin(angle) * vertical_squash
        sx, sy = int(round(x)), int(round(y))

        if 0 <= sx < width and 0 <= sy < height:
            depth_factor = 1 - radius / max_radius
            char_idx = int(depth_factor * (len(chars)-1))
            ch = chars[char_idx]
            color = 16 + int(depth_factor * 215)
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
