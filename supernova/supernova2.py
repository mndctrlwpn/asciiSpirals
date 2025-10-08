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

# Symbols for different particle types
symbols = ['*', '+', '.', 'o', '@', '%', '#', '&']

class Particle:
    def __init__(self, x, y, vx, vy, color, lifetime, symbol):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.lifetime = lifetime
        self.symbol = symbol

    def update(self):
        # Add turbulence to velocity
        self.vx += random.uniform(-0.05, 0.05)
        self.vy += random.uniform(-0.05, 0.05)
        self.x += self.vx
        self.y += self.vy
        self.lifetime -= 1

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def generate_particles(center_x, center_y, num_particles, dense=True):
    particles = []
    for _ in range(num_particles):
        angle = random.uniform(0, 2*math.pi)
        # Dense particles mostly near center, some scattered farther
        r = random.uniform(0, 1 if dense else 5)
        speed = r * random.uniform(0.2, 2.0)
        vx = speed * math.cos(angle)
        vy = speed * math.sin(angle)
        color = random.choice(colors)
        lifetime = random.randint(50, 500)
        symbol = random.choice(symbols)
        particles.append(Particle(center_x, center_y, vx, vy, color, lifetime, symbol))
    return particles

def draw_frame(particles, width, height):
    grid = [[' ' for _ in range(width)] for _ in range(height)]
    color_grid = [['' for _ in range(width)] for _ in range(height)]
    for p in particles:
        x, y = int(p.x), int(p.y)
        if 0 <= x < width and 0 <= y < height:
            grid[y][x] = p.symbol
            color_grid[y][x] = p.color
    lines = []
    for y in range(height):
        line = ''
        for x in range(width):
            if grid[y][x] != ' ':
                line += f"{color_grid[y][x]}{grid[y][x]}{RESET}"
            else:
                # Random dark globules for supernova remnants
                if random.random() < 0.02:
                    line += '.'
                else:
                    line += ' '
        lines.append(line)
    return '\n'.join(lines)

def supernova_simulation():
    size = shutil.get_terminal_size()
    width, height = size.columns, size.lines
    center_x, center_y = width // 2, height // 2

    # Initial dense cloud
    particles = generate_particles(center_x, center_y, 5000)

    try:
        while True:
            print("/033[H", end='') # Move cursor to top-left
            print(draw_frame(particles, width, height))
            time.sleep(0.03)

            # Update all particles
            for p in particles:
                p.update()

            # Remove dead particles
            particles = [p for p in particles if p.lifetime > 0]

            # Continuously spawn new particles for psychedelic chaos
            if random.random() < 0.5:
                particles.extend(generate_particles(center_x, center_y, random.randint(50, 200)))

            # Slightly increase center turbulence for dark globules
            if random.random() < 0.05:
                particles.extend(generate_particles(center_x, center_y, random.randint(5, 20), dense=False))

    except KeyboardInterrupt:
        clear_screen()
        sys.exit()

if __name__ == "__main__":
    supernova_simulation()
