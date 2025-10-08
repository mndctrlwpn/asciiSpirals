import os
import sys
import time
import random
import math
import shutil

# Bright ANSI colors for plasma
colors = [
    '\033[91m',  # Red
    '\033[93m',  # Yellow
    '\033[97m',  # White
    '\033[94m',  # Blue
    '\033[95m',  # Magenta
    '\033[96m',  # Cyan
]

RESET = '\033[0m'
symbols = ['*', '+', '.', 'o', '@', '%', '#', '&']

class Particle:
    def __init__(self, x, y, vx, vy, color, lifetime, symbol, is_globule=False, is_spiral=False):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.lifetime = lifetime
        self.symbol = symbol
        self.is_globule = is_globule
        self.is_spiral = is_spiral

    def update(self):
        # Chaos turbulence
        self.vx += random.uniform(-0.03, 0.03)
        self.vy += random.uniform(-0.03, 0.03)

        if self.is_spiral:
            cx, cy = self.center
            dx = self.x - cx
            dy = self.y - cy
            r = math.hypot(dx, dy) + 0.0001
            angle = math.atan2(dy, dx)
            
            # Stronger angular push along spiral
            spiral_strength = 1  # was 0.05 before
            angle += spiral_strength
            
            # Slight radial correction to hug spiral
            radial_correction = 0.02
            self.vx += -dx * radial_correction / r
            self.vy += -dy * radial_correction / r
            
            speed = math.hypot(self.vx, self.vy) or 0.3
            self.vx = speed * math.cos(angle)
            self.vy = speed * math.sin(angle)

        self.x += self.vx
        self.y += self.vy
        self.lifetime -= 1

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def generate_particles(center_x, center_y, num_particles, dense=True, globule=False, spiral=False):
    particles = []
    for _ in range(num_particles):
        angle = random.uniform(0, 2*math.pi)
        r = random.uniform(0, 1 if dense else 5)
        speed = r * random.uniform(0.2, 2.0)
        vx = speed * math.cos(angle)
        vy = speed * math.sin(angle)
        color = random.choice(colors) if not globule else '\033[90m'
        lifetime = random.randint(50, 500)
        symbol = random.choice(symbols) if not globule else ' '
        p = Particle(center_x, center_y, vx, vy, color, lifetime, symbol, is_globule=globule, is_spiral=spiral)
        if spiral:
            p.center = (center_x, center_y)
        particles.append(p)
    return particles

def draw_frame(particles, width, height):
    grid = [[' ' for _ in range(width)] for _ in range(height)]
    color_grid = [['' for _ in range(width)] for _ in range(height)]

    for p in particles:
        x, y = int(p.x), int(p.y)
        if 0 <= x < width and 0 <= y < height:
            grid[y][x] = p.symbol
            color_grid[y][x] = p.color

    # Globules cluster effect
    for p in [pt for pt in particles if pt.is_globule]:
        gx, gy = int(p.x), int(p.y)
        for dx in range(-2, 3):
            for dy in range(-2, 3):
                nx, ny = gx + dx, gy + dy
                if 0 <= nx < width and 0 <= ny < height:
                    if random.random() < 0.5:
                        grid[ny][nx] = ' '
                        color_grid[ny][nx] = '\033[90m'

    lines = []
    for y in range(height):
        line = ''
        for x in range(width):
            if grid[y][x] != ' ':
                line += f"{color_grid[y][x]}{grid[y][x]}{RESET}"
            else:
                line += ' '
        lines.append(line)
    return '\n'.join(lines)

def supernova_simulation():
    size = shutil.get_terminal_size()
    width, height = size.columns, size.lines
    center_x, center_y = width // 2, height // 2

    particles = generate_particles(center_x, center_y, 5000)

    # Initial globules
    for _ in range(5):
        particles.extend(generate_particles(center_x, center_y, random.randint(30, 80), globule=True))

    # Stronger spiral thread
    particles.extend(generate_particles(center_x, center_y, 600, spiral=True))  # increased count

    try:
        while True:
            print("\033[H", end='')
            print(draw_frame(particles, width, height))
            time.sleep(0.03)

            for p in particles:
                p.update()

            particles = [p for p in particles if p.lifetime > 0]

            # Chaos spawning
            if random.random() < 0.5:
                particles.extend(generate_particles(center_x, center_y, random.randint(50, 200)))
            if random.random() < 0.1:
                particles.extend(generate_particles(center_x, center_y, random.randint(10, 30), globule=True))
            if random.random() < 0.05:
                particles.extend(generate_particles(center_x, center_y, random.randint(10, 30), spiral=True))

    except KeyboardInterrupt:
        clear_screen()
        sys.exit()

if __name__ == "__main__":
    supernova_simulation()
