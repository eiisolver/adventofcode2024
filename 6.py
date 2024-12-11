from collections import defaultdict
from typing import Dict, Tuple
from grid import Grid, NESW, Pos

lines = open("6_input.txt", "r").read().splitlines()
grid = Grid.create(lines)


def next(pos: Pos, dir: int) -> Pos:
    return pos.add(NESW.DIRS[dir])


def patrol(start_pos: Pos, dir: int) -> Tuple[Dict, Pos]:
    """
    Performs a guard's control. Stops when outside grid, or when loop is detected.
    Returns visited places + last position.
    """
    visited = defaultdict(set)
    curr_pos = start_pos
    while grid.contains(curr_pos) and dir not in visited[curr_pos]:
        visited[curr_pos].add(dir)
        next_pos = next(curr_pos, dir)
        while grid.contains(next_pos) and next_pos.at(lines) == "#":
            dir = (dir + 1) % 4
            next_pos = next(curr_pos, dir)
        curr_pos = next_pos
    return visited, curr_pos


start_pos = None
for pos in grid.positions():
    if pos.at(lines) == "^":
        start_pos = pos

visited, final_pos = patrol(start_pos, 0)
print("Part 1:", len(visited))

looping_obstacles = set()
for obstacle in visited:
    # Place obstacle and perform new patrol
    old_line = lines[obstacle.row]
    new_line = old_line[: obstacle.col] + "#" + old_line[obstacle.col + 1 :]
    lines[obstacle.row] = new_line
    _, final_pos = patrol(start_pos, 0)
    # Restore
    lines[obstacle.row] = old_line
    if grid.contains(final_pos):
        # Patrol ended on grid, so a loop was detected
        looping_obstacles.add(obstacle)
print("Part 2:", len(looping_obstacles))
