import curses
import random
import math
import time

# Particle class
class Particle:
    def __init__(self, x, y, vx, vy, symbol, color, lifetime, kind='disk'):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.symbol = symbol
        self.color = color
        self.lifetime = lifetime
        self.kind = kind  # 'disk', 'globule', 'supernova'

    def update(self, cx, cy, center_radius, spiral_strength, turbulence):
        dx = self.x - cx
        dy = self.y - cy
        r = math.hypot(dx, dy) + 0.0001

        # Chaos turbulence
        self.vx += random.uniform(-turbulence, turbulence)
        self.vy += random.uniform(-turbulence, turbulence)

        # Gravity toward center (black hole)
        g_strength = 0.002 if self.kind != 'disk' else 0.0
        self.vx -= g_strength * dx / r
        self.vy -= g_strength * dy / r

        # Tangential spiral rotation
        if self.kind == 'disk' or self.kind == 'supernova':
            angle = math.atan2(dy, dx)
            speed = math.hypot(self.vx, self.vy) or 0.1
            angle += spiral_strength
            self.vx = speed * math.cos(angle)
            self.vy = speed * math.sin(angle)

        self.x += self.vx
        self.y += self.vy
        self.lifetime -= 1

# Generate particles
def generate_particles(cx, cy, num, kind='supernova'):
    particles = []
    colors = {
        'disk': [curses.COLOR_YELLOW, curses.COLOR_MAGENTA, curses.COLOR_WHITE, curses.COLOR_CYAN],
        'globule': [curses.COLOR_BLACK],
        'supernova': [curses.COLOR_RED, curses.COLOR_YELLOW, curses.COLOR_WHITE,
                      curses.COLOR_MAGENTA, curses.COLOR_CYAN]
    }
    symbols = {
        'disk': ['*', '+', 'o', '@'],
        'globule': [' '],
        'supernova': ['*', '+', '.', 'o', '@', '%', '#', '&']
    }
    for _ in range(num):
        # Random offset from center for implosion + chaotic supernova
        r0 = random.uniform(0.5, 8)  # wider initial cloud
        angle0 = random.uniform(0, 2*math.pi)
        x = cx + r0 * math.cos(angle0)
        y = cy + r0 * math.sin(angle0)

        # Tangential velocity for spiral effect
        speed = random.uniform(0.5, 2.5)
        vx = -speed * math.sin(angle0)
        vy = speed * math.cos(angle0)

        symbol = random.choice(symbols[kind])
        color = random.choice(colors[kind])
        lifetime = random.randint(1000, 4000)
        particles.append(Particle(x, y, vx, vy, symbol, color, lifetime, kind))
    return particles

# Draw frame
def draw_frame(stdscr, particles, width, height):
    grid = [[' ' for _ in range(width)] for _ in range(height)]
    color_grid = [[0 for _ in range(width)] for _ in range(height)]
    for p in particles:
        x, y = int(p.x), int(p.y)
        if 0 <= x < width and 0 <= y < height:
            grid[y][x] = p.symbol
            color_grid[y][x] = p.color
    for y in range(height):
        for x in range(width):
            try:
                stdscr.addch(y, x, grid[y][x], curses.color_pair(color_grid[y][x]))
            except curses.error:
                pass

# Main simulation
def galaxy_simulation(stdscr):
    curses.curs_set(0)
    curses.start_color()
    curses.use_default_colors()
    for i in range(0, curses.COLORS):
        curses.init_pair(i+1, i, -1)

    height, width = stdscr.getmaxyx()
    cx, cy = width // 2, height // 2
    center_radius = 3

    # Immediate imploding star + dense supernova
    particles = generate_particles(cx, cy, 6000, 'supernova')   # dense supernova
    particles.extend(generate_particles(cx, cy, 500, 'disk'))    # disk/spiral seeds
    particles.extend(generate_particles(cx, cy, 200, 'globule')) # dark remnants

    start_time = time.time()
    duration = 30*60  # ~30 minutes real-time evolution
    spiral_strength = 0.05
    turbulence = 0.05

    while True:
        stdscr.erase()
        height, width = stdscr.getmaxyx()
        cx, cy = width // 2, height // 2

        elapsed = time.time() - start_time
        # Strengthen spiral and reduce turbulence over time
        spiral_strength = min(0.15, 0.05 + 0.1*(elapsed/duration))
        turbulence = max(0.01, 0.05 - 0.04*(elapsed/duration))

        for p in particles:
            p.update(cx, cy, center_radius, spiral_strength, turbulence)

        # Absorb particles into central black hole
        new_particles = []
        for p in particles:
            if p.kind != 'globule' and math.hypot(p.x-cx, p.y-cy) < center_radius:
                continue
            if p.lifetime > 0:
                new_particles.append(p)
        particles = new_particles

        # Spawn additional particles for chaotic effect
        if random.random() < 0.3:
            particles.extend(generate_particles(cx, cy, random.randint(20, 50), 'supernova'))
        if random.random() < 0.02:
            particles.extend(generate_particles(cx, cy, random.randint(5, 15), 'disk'))
        if random.random() < 0.02:
            particles.extend(generate_particles(cx, cy, random.randint(2, 5), 'globule'))

        draw_frame(stdscr, particles, width, height)
        stdscr.refresh()
        time.sleep(0.03)

if __name__ == "__main__":
    curses.wrapper(galaxy_simulation)
