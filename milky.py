#!/usr/bin/env python3
# milky_way_ascii_responsive.py — Animated Milky Way, adjusts to terminal size

import math
import time
import shutil
import sys
import random

chars = " .:-=+*#%@"
frame_delay = 0.05
vertical_squash = 0.25
num_arms = 4
arm_spread = 0.2
arm_turns = 4
core_radius_frac = 0.1
black_hole_radius_frac = 0.02
star_density = 4000
rotation_speed_core = 0.08
rotation_speed_outer = 0.02
rotation_direction = 1  # 1 = CCW, -1 = CW

def clear_screen():
    sys.stdout.write("\033[2J\033[H")
    sys.stdout.flush()

def generate_stars():
    stars = []
    for _ in range(star_density):
        if random.random() < 0.2:  # core stars
            r_frac = random.random() * core_radius_frac
            theta = random.uniform(0, 2*math.pi)
        else:
            arm = random.randint(0, num_arms-1)
            t = random.random()
            r_frac = core_radius_frac + t * (1 - core_radius_frac)
            base_angle = arm * 2*math.pi/num_arms + math.log(r_frac*100+1)*arm_turns
            theta = base_angle + random.uniform(-arm_spread, arm_spread)

        if r_frac < black_hole_radius_frac:
            continue

        depth = 1 - r_frac + random.uniform(-0.05, 0.05)
        depth = max(0, min(1, depth))
        char_idx = int(depth * (len(chars)-1))
        ch = chars[char_idx]

        stars.append({
            "r_frac": r_frac,  # store as fraction of max radius
            "theta": theta,
            "depth": depth,
            "char": ch
        })
    return stars

def draw_frame(stars):
    size = shutil.get_terminal_size(fallback=(120,50))
    width, height = size.columns, size.lines
    cx, cy = width//2, height//2
    max_radius = min(cx, int(cy/vertical_squash)) - 2

    screen = [[" "]*width for _ in range(height)]

    for star in stars:
        r = star["r_frac"] * max_radius
        speed = rotation_speed_core * (1 - star["r_frac"]) + rotation_speed_outer * star["r_frac"]
        star["theta"] -= rotation_direction * speed

        x = cx + r * math.cos(star["theta"])
        y = cy + r * math.sin(star["theta"]) * vertical_squash

        sx, sy = int(round(x)), int(round(y))
        if 0 <= sx < width and 0 <= sy < height:
            depth = min(1.0, max(0.0, star["depth"] + random.uniform(-0.02, 0.02)))
            char_idx = int(depth * (len(chars)-1))
            ch = chars[char_idx]
            color = 16 + int(depth*215)
            screen[sy][sx] = f"\033[38;5;{color}m{ch}\033[0m"

    sys.stdout.write("\033[H")
    for row in screen:
        sys.stdout.write("".join(row) + "\n")
    sys.stdout.flush()

def main():
    clear_screen()
    stars = generate_stars()
    try:
        while True:
            draw_frame(stars)
            time.sleep(frame_delay)
    except KeyboardInterrupt:
        sys.stdout.write("\033[0m\n")
        sys.exit()

if __name__ == "__main__":
    main()
