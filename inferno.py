import math, os, sys, time, shutil, colorsys

# ---- Color handling ----
def hsv_to_ansi(h, s, v):
    r, g, b = [int(x * 5) for x in colorsys.hsv_to_rgb(h % 1.0, s, v)]
    return 16 + 36*r + 6*g + b

def clear():
    sys.stdout.write("\033[H\033[J")

# ---- Spiral drawing ----
def draw_spiral(t, cols, rows):
    cx, cy = cols // 2, rows // 2
    frame = [[' ' for _ in range(cols)] for _ in range(rows)]

    phi = (1 + 5 ** 0.5) / 2  # golden ratio
    base_radius = min(cols, rows) / 2.5
    chars = " .:-=+*#%@"
    density = len(chars) - 1

    # Golden spiral equation in polar: r = a * φ^(bθ)
    a = base_radius * 0.02
    b = 1 / (2 * math.pi)
    max_theta = 8 * math.pi
    step = 0.05

    for i in range(int(max_theta / step)):
        θ = -i * step + t * 0.6  # negative for counterclockwise spin
        r = a * (phi ** (b * θ))
        x = int(cx + r * math.cos(θ))
        y = int(cy + r * math.sin(θ) * 0.55)  # vertical compression for terminal aspect ratio
        if 0 <= x < cols and 0 <= y < rows:
            frame[y][x] = chars[int((i / (max_theta / step)) * density)]

    # ---- Render with color phase ----
    output = []
    color_phase = (t * 0.25) % 1.0
    for y in range(rows):
        for x in range(cols):
            ch = frame[y][x]
            if ch != ' ':
                angle = math.atan2(y - cy, x - cx)
                hue = ((angle / (2 * math.pi)) + color_phase) % 1.0
                color = hsv_to_ansi(hue, 1.0, 1.0)
                output.append(f"\033[38;5;{color}m{ch}")
            else:
                output.append(" ")
        output.append("\033[0m\n")

    sys.stdout.write(''.join(output))
    sys.stdout.flush()

# ---- Main loop ----
def main():
    try:
        t = 0
        while True:
            cols, rows = shutil.get_terminal_size()
            clear()
            draw_spiral(t, cols, rows)
            t += 0.07
            time.sleep(0.05)
    except KeyboardInterrupt:
        clear()
        sys.exit(0)

if __name__ == "__main__":
    main()
