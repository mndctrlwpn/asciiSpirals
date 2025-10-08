#!/usr/bin/env python3
"""
spiral_from_ascii.py

Pre-rendered large ASCII art (vortex) is embedded below. This script scales the art
to your terminal, and animates it into a counter-clockwise spiral with dynamic
tie-dye truecolor (or 256-color fallback). Background color is unchanged.

Usage:
    python3 spiral_from_ascii.py
    python3 spiral_from_ascii.py --256   # force 256-color fallback

Ctrl+C to quit.
"""

import os, sys, time, math, shutil, signal

# -------------------------
# PRE-RENDERED ASCII ART
# (Large, bright vortex; the two shadow figures removed)
# Width ~120 cols, Height ~46 rows (will be scaled to fit terminal)
# -------------------------
ART = r"""
........................................................................................................
...........................................:::::::=*#%@@%#*+=:..........................................
.....................................:::::::-=+*#%@@@@@@@@@@@@%#*+=-:...................................
..................................:::::::-=+*#%@@@@@@@@@@@@@@@@@@@@%#*+=-::..............................
...............................:::::::-=+*#%@@@@@@@@@@@@@@@@@@@@@@@@@@@@%#*+=-::.........................
.............................:::::::-=+*#%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%#*+=-::...................
...........................:::::::-=+*#%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%#*+=-::...............
.........................:::::::-=+*#%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%#*+=-::.............
.......................:::::::-=+*#%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%#*+=-::..........
......................:::::::-=+*#%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%#*+=-:......
....................:::::::-=+*#%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%#*+=-:....
...................:::::::-=+*#%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%#*+=-:
..................:::::::-=+*#%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%#*+=
.................:::::::-=+*#%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%#
................:::::::-=+*#%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
...............:::::::-=+*#%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
..............:::::::-=+*#%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
.............:::::::-=+*#%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%
............:::::::-=+*#%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%@
...........:::::::-=+*#%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%@@
..........:::::::-=+*#%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%@@@
.........:::::::-=+*#%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%@@@
........:::::::-=+*#%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%@@@
.......:::::::-=+*#%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%@@@
......:::::::-=+*#%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%@@@
.....:::::::-=+*#%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%@@@
....:::::::-=+*#%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%@@@
...:::::::-=+*#%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%@@@@
..:::::::-=+*#%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%@@@@
.:::::::-=+*#%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%@@@@
:::::::-=+*#%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%@@@@
:::::::-=+*#%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%@@@@
.:::::::-=+*#%@@@@@@@@@@@%%%%%%%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%@@@@
..:::::::-=+*#%@@@@@%*=-:......:-=+*#%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%@@@@
...:::::::-=+*#%@@#=:..............:-=+*#%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%@@@@
....:::::::-=+*#*=:....................:-=+*#%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%@@@@
.....:::::::-=+*=-:......................:-=+*#%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%@@@@
......:::::::-=+:-:........................:-=+*#%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%@@@@@
.......:::::::-:............................:-=+*#%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%@@@@@
........:::::::-:.............................:-=+*#%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%@@@@@@
.........:::::::::..............................:-=+*#%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%@@@@@@@
..........:::::::::...............................:-=+*#%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%@@@@@@@@
...........::::::::::.................................:-=+*#%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%@@@@@@@@@@@
............:::::::::::.................................:-=+*#%@@@@@@@@@@@@@@@@@@@@@@@@@@%@@@@@@@@@@@@@@@
.............:::::::::::::.................................:-=+*#%@@@@@@@@@@@@@@@@@@@@%@@@@@@@@@@@@@@@@@@
..............::::::::::::::.................................:-=+*#%@@@@@@@@@@@@@@@%@@@@@@@@@@@@@@@@@@@@@
...............:::::::::::::::::.................................:-=+*#%@@@@@@@@@@@%@@@@@@@@@@@@@@@@@@@@@@
................::::::::::::::::::.................................:-=+*#%@@@@@%@@@@@@@@@@@@@@@@@@@@@@@@@
.................:::::::::::::::::::::.................................:-=+*#%@@%@@@@@@@@@@@@@@@@@@@@@@@@@
..................::::::::::::::::::::::.................................:-=+*#%@@@@@@@@@@@@@@@@@@@@@@@@@@
....................:::::::::::::::::::::::................................:-=+*#%@@@@@@@@@@@@@@@@@@@@@@@
........................................................................................................
"""  # end ART

# -------------------------
# Terminal/color utilities
# -------------------------
def supports_truecolor():
    ct = os.environ.get("COLORTERM", "").lower()
    if "truecolor" in ct or "24bit" in ct:
        return True
    # assume truecolor for modern envs; user can force --256
    return True

def hide_cursor():
    sys.stdout.write("\033[?25l")
def show_cursor():
    sys.stdout.write("\033[?25h")
def move_cursor_home():
    sys.stdout.write("\033[H")
def clear_screen():
    sys.stdout.write("\033[2J")
def flush():
    sys.stdout.flush()

# convert hsv (0..1) to RGB (0..255)
def hsv_to_rgb(h, s, v):
    if s == 0.0:
        r = g = b = int(v * 255)
        return r, g, b
    i = int(h * 6.0)  # assume h in [0,1)
    f = (h * 6.0) - i
    p = v * (1.0 - s)
    q = v * (1.0 - s * f)
    t = v * (1.0 - s * (1.0 - f))
    i = i % 6
    if i == 0:
        r, g, b = v, t, p
    elif i == 1:
        r, g, b = q, v, p
    elif i == 2:
        r, g, b = p, v, t
    elif i == 3:
        r, g, b = p, q, v
    elif i == 4:
        r, g, b = t, p, v
    else:
        r, g, b = v, p, q
    return int(r * 255), int(g * 255), int(b * 255)

def rgb_to_truecolor_seq(r,g,b):
    return f"\033[38;2;{r};{g};{b}m"

def rgb_to_256(r,g,b):
    # map 0..255 to xterm 256 cube 16..231
    r6 = int((r/255.0)*5 + 0.5)
    g6 = int((g/255.0)*5 + 0.5)
    b6 = int((b/255.0)*5 + 0.5)
    code = 16 + 36*r6 + 6*g6 + b6
    return f"\033[38;5;{code}m"

# -------------------------
# ASCII art processing & scaling
# -------------------------
# Convert ART into a 2D list of characters (lines may be ragged -> pad)
art_lines = [line.rstrip("\n") for line in ART.splitlines() if line.strip("\n") != ""]
orig_h = len(art_lines)
orig_w = max(len(line) for line in art_lines)
# pad lines to same width
for i in range(len(art_lines)):
    art_lines[i] = art_lines[i].ljust(orig_w)

# Character cell aspect adjustment (terminal characters are typically taller than wide)
CHAR_ASPECT = 0.5  # approximate width/height ratio for chars (tweak if needed)

def get_terminal_size():
    cols, rows = shutil.get_terminal_size((80,24))
    return cols, rows

def scale_art_to_terminal(cols, rows):
    # rows: available rows for art (we'll reserve 1 row for status)
    # We want art to nearly fill the terminal width (outer arms nearly touching edges).
    target_w = max(20, cols)
    # determine height based on char aspect
    # char cells are taller; compute target_h in lines to preserve art aspect
    art_ratio = orig_h / orig_w  # height/width
    # desired pixel-like height in character rows:
    target_h = int(target_w * art_ratio * CHAR_ASPECT)
    if target_h > rows - 1:
        target_h = rows - 1
        target_w = max(20, int(target_h / (art_ratio * CHAR_ASPECT)))
    # clamp
    if target_w < 20: target_w = 20
    if target_h < 8: target_h = 8

    # simple nearest-neighbor scale from original art to target_w x target_h
    scaled = []
    for y in range(target_h):
        row_chars = []
        sy = y / float(max(1, target_h-1)) * (orig_h - 1)
        sy_i = int(round(sy))
        for x in range(target_w):
            sx = x / float(max(1, target_w-1)) * (orig_w - 1)
            sx_i = int(round(sx))
            row_chars.append(art_lines[sy_i][sx_i])
        scaled.append(row_chars)
    return scaled

# -------------------------
# Spiral transform & animation
# -------------------------
def run_animation(force_256=False):
    use_true = supports_truecolor() and not force_256
    cols, rows = get_terminal_size()
    rows_avail = rows
    scaled = scale_art_to_terminal(cols, rows_avail)

    H = len(scaled)
    W = len(scaled[0])
    cx = (W - 1) / 2.0
    cy = (H - 1) / 2.0
    max_r = math.hypot(cx, cy)

    FPS = 20.0
    delay = 1.0 / FPS
    swirl_speed = 0.06      # rotation speed
    spiral_strength = 1.2   # how dramatic the spiral distortion is
    outward_speed = 0.25    # how fast the spiral radiates outward

    time0 = time.time()

    # Precompute base characters
    base_chars = [[scaled[y][x] for x in range(W)] for y in range(H)]

    # Hide cursor + clear
    hide_cursor()
    clear_screen()
    try:
        while True:
            t = time.time() - time0

            # Handle dynamic resizing
            new_cols, new_rows = get_terminal_size()
            if new_cols != cols or new_rows != rows:
                cols, rows = new_cols, new_rows
                rows_avail = rows
                scaled = scale_art_to_terminal(cols, rows_avail)
                H = len(scaled)
                W = len(scaled[0])
                cx = (W - 1) / 2.0
                cy = (H - 1) / 2.0
                max_r = math.hypot(cx, cy)
                base_chars = [[scaled[y][x] for x in range(W)] for y in range(H)]

            move_cursor_home()
            out_lines = []

            for y in range(H):
                parts = []
                for x in range(W):
                    # Compute normalized polar coords from center
                    rx = x - cx
                    ry = y - cy
                    r = math.hypot(rx, ry) / max_r
                    ang = math.atan2(ry, rx)

                    # Outward radial motion
                    r_out = (r + outward_speed * t) % 1.0

                    # Spiral rotation (counter-clockwise)
                    rot = swirl_speed * t + r_out * spiral_strength
                    new_ang = ang - rot + math.sin(t*0.8 + r_out*10.0)*0.2

                    # Map back to Cartesian coordinates
                    rx_new = r_out * max_r * math.cos(new_ang)
                    ry_new = r_out * max_r * math.sin(new_ang)
                    x_disp = int(round(cx + rx_new))
                    y_disp = int(round(cy + ry_new))

                    # Sample ASCII character
                    if 0 <= x_disp < W and 0 <= y_disp < H:
                        ch = base_chars[y_disp][x_disp]
                    else:
                        ch = " "

                    # Skip spaces for performance
                    if ch == " ":
                        parts.append(" ")
                        continue

                    # Color calculation (tie-dye effect)
                    hue = ((new_ang / (2*math.pi)) + (t*0.08) + (r_out*2.5)) % 1.0
                    sat = max(0.2, min(1.0, 0.9 - r_out*0.6))
                    val = max(0.15, min(1.0, 0.85 - 0.25*(1.0 - r_out) + 0.12*math.sin(t*2.0 + r_out*15.0)))
                    rcol, gcol, bcol = hsv_to_rgb(hue, sat, val)
                    if use_true:
                        seq = rgb_to_truecolor_seq(rcol, gcol, bcol)
                    else:
                        seq = rgb_to_256(rcol, gcol, bcol)
                    parts.append(f"{seq}{ch}\033[0m")
                out_lines.append("".join(parts))
            sys.stdout.write("\n".join(out_lines))
            flush()

            # Sleep for next frame
            time_spent = (time.time() - time0) - t
            sleep_time = max(0.0, delay - time_spent)
            time.sleep(sleep_time)

    except KeyboardInterrupt:
        move_cursor_home()
        clear_screen()
        show_cursor()
        print("Exited.")
    except Exception as e:
        show_cursor()
        clear_screen()
        raise
                    

# -------------------------
# Entry point
# -------------------------
if __name__ == "__main__":
    force256 = ("--256" in sys.argv)
    # handle SIGWINCH on Unix (terminal resize) gracefully by continuing loop which re-checks size
    try:
        run_animation(force256)
    except Exception as e:
        show_cursor()
        clear_screen()
        print("Error:", e)
        sys.exit(1)
