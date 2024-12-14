import re
import numpy as np
import pygame as pg

from grid import Pos
from dataclasses import dataclass

file_name = "14_input.txt"
lines = open(file_name, "r").read().splitlines()

area = Pos(7, 11) if "test" in file_name else Pos(103, 101)
middle = Pos(area.row // 2, area.col // 2)


@dataclass
class Robot:
    pos: Pos
    v: Pos


def quadrant(pos: Pos) -> int:
    if pos.row == middle.row or pos.col == middle.col:
        return None
    return 2 * (pos.row // (middle.row + 1)) + pos.col // (middle.col + 1)


robots: list[Robot] = []
for line in lines:
    nrs = [int(nr) for nr in re.findall("[-]?\d+", line)]
    robots.append(Robot(Pos(nrs[1], nrs[0]), Pos(nrs[3], nrs[2])))

positions = [r.pos.add(r.v.multiply(100)).wrap(area) for r in robots]
robots_per_quadrant = 4 * [0]
for pos in positions:
    q = quadrant(pos)
    if q is not None:
        robots_per_quadrant[q] += 1
print("Part 1:", np.prod(robots_per_quadrant))


def draw(win, robots, t):
    """
    Draws position of robots at time t on pygame window.
    """
    pixels = 3
    white = (255, 255, 255)
    green = (53, 94, 64)
    positions = [r.pos.add(r.v.multiply(t)).wrap(area) for r in robots]
    win.fill(white)
    radius = 2
    print("Time:", t)
    for p in positions:
        pg.draw.circle(win, green, (pixels * p.col, 50 + pixels * p.row), radius)
    pg.display.flip()


# create the display window
width = 500
height = 500
win = pg.display.set_mode((width, height))
# optional title bar caption
pg.display.set_caption("Pygame")

# (press escape key or click window title bar x to exit)
t = 0
draw(win, robots, t)
while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            # most reliable exit on x click
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            # optional exit with escape key
            if event.key == pg.K_ESCAPE:
                pg.quit()
                raise SystemExit
            c = chr(event.key)
            if c == "-":
                t -= 1
            elif c == "1":
                t += 10
            elif c == "2":
                t += 101
            elif c == "0":
                t -= 10
            elif c == "9":
                t -= 101
            elif c == "e":
                ## easter egg
                t = 6577
            else:
                t += 1
            draw(win, robots, t)
