from itertools import pairwise
from grid import Grid, Pos, NESW
import functools

lines = open("21_input.txt", "r").read().splitlines()

NUM_KEYPAD = ["789", "456", "123", "#0A"]
DIR_NAMES = "^>v<A"

# Best paths, calculated by hand, after having read notes on reddit.
DIR_REVERSE = {
    "AA": "",
    "A<": "v<<",
    "A>": "v",
    "A^": "<",
    "Av": "<v",
    "<A": ">>^",
    "<<": "",
    "<>": ">>",
    "<^": ">^",
    "<v": ">",
    ">A": "^",
    "><": "<<",
    ">>": "",
    ">^": "<^",
    ">v": "<",
    "^A": ">",
    "^<": "v<",
    "^>": "v>",
    "^^": "",
    "^v": "v",
    "vA": "^>",
    "v<": "<",
    "v>": ">",
    "v^": "^",
    "vv": "",
}

num_grid = Grid.create(NUM_KEYPAD)
num_pos: dict[str, Pos] = {pos.at(NUM_KEYPAD): pos for pos in num_grid.positions()}


@functools.cache
def dir_shortest_path(actions: str, depth) -> int:
    """
    Returns number of keys required to gnerate the given actions on the directional
    keyboard, with depth underlying directional robots.
    """
    if depth == 0:
        return len(actions)
    result = sum(dir_shortest_path(DIR_REVERSE[fr + to] + "A", depth - 1) for fr, to in pairwise("A" + actions))
    return result


def num_shortest_path(actions: str, from_pos: Pos, to_pos: Pos, depth: int) -> int:
    """
    Returns number of keys required to generate the given actions on the numeric keyboard,
    with depth underlying directional robots.

    Recursive function that tests all paths from from_pos to to_pos.
    """
    if from_pos == to_pos:
        return dir_shortest_path(actions + "A", depth)
    dist = from_pos.manhattan(to_pos)
    best = None
    for dir in range(4):
        pos = from_pos + NESW.DIRS[dir]
        if num_grid.contains(pos) and pos.manhattan(to_pos) == dist - 1 and pos.at(NUM_KEYPAD) != "#":
            v = num_shortest_path(actions + DIR_NAMES[dir], pos, to_pos, depth)
            if best is None or v < best:
                best = v
    return best


for robots in (2, 25):
    part = 0
    for code in lines:
        n = sum(num_shortest_path("", num_pos[fr], num_pos[to], robots) for fr, to in pairwise("A" + code))
        print(code, n)
        part += int(code[:3]) * n

    print("Result for", robots, "robots:", part)
