import os
import sys
import time
import random
import math
import shutil

# ANSI colors for supernova layers
colors = [
    '\033[91m',  # Red
    '\033[93m',  # Yellow
    '\033[97m',  # White
    '\033[94m',  # Blue
    '\033[95m',  # Magenta
]

RESET = '\033[0m'
symbols = ['*', '+', '.', 'o', '@', '%', '#']

class Particle:
    def __init__(self, x, y, vx, vy, color, lifetime):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.lifetime = lifetime

    def update(self):
        # Update position with some turbulence
        self.x += self.vx + random.uniform(-0.05, 0.05)
        self.y += self.vy + random.uniform(-0.05, 0.05)
        self.lifetime -= 1

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def generate_particles(center_x, center_y, num_particles):
    particles = []
    for _ in range(num_particles):
        angle = random.uniform(0, 2*math.pi)
        speed = random.uniform(0.05, 1.5)
        vx = speed * math.cos(angle)
        vy = speed * math.sin(angle)
        color = random.choice(colors)
        lifetime = random.randint(50, 300)
        particles.append(Particle(center_x, center_y, vx, vy, color, lifetime))
    return particles

def draw_frame(particles, width, height):
    grid = [[' ' for _ in range(width)] for _ in range(height)]
    color_grid = [['' for _ in range(width)] for _ in range(height)]
    for p in particles:
        x, y = int(p.x), int(p.y)
        if 0 <= x < width and 0 <= y < height:
            grid[y][x] = random.choice(symbols)
            color_grid[y][x] = p.color
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
    # Terminal size
    size = shutil.get_terminal_size()
    width, height = size.columns, size.lines
    center_x, center_y = width // 2, height // 2

    # Initial particles
    particles = generate_particles(center_x, center_y, 1500)  # Much denser

    try:
        while particles:
            clear_screen()
            print(draw_frame(particles, width, height))
            time.sleep(0.03)  # Slightly faster for smoother motion

            # Update particles
            for p in particles:
                p.update()

            # Remove dead particles
            particles = [p for p in particles if p.lifetime > 0]

            # Continuously spawn a few new particles for ongoing explosion
            if random.random() < 0.2:
                particles.extend(generate_particles(center_x, center_y, random.randint(10, 30)))

    except KeyboardInterrupt:
        clear_screen()
        sys.exit()

if __name__ == "__main__":
    supernova_simulation()
