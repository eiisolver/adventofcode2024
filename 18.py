import functools
from grid import Grid, NESW, Pos
import graph

file_name = "18_input.txt"
bytes_str = [line.split(",") for line in open(file_name, "r").read().splitlines()]
falling_bytes: list[Pos] = [Pos(int(nr[1]), int(nr[0])) for nr in bytes_str]

if "test" in file_name:
    grid = Grid(7, 7)
    nr_bytes = 12
else:
    grid = Grid(71, 71)
    nr_bytes = 1024

end_pos = Pos(grid.rows - 1, grid.cols - 1)
corrupt_positions: set[Pos] = set(falling_bytes[:nr_bytes])


def neighbours(pos: Pos) -> list[Pos]:
    return [n for n in pos.neighbours(NESW.DIRS) if grid.contains(n) and n not in corrupt_positions]


distances = graph.flood_fill({Pos(0, 0)}, neighbours)
print("Part 1:", distances[end_pos])

# Part 2: just repeat doing flood fills until failure.
corrupt_positions = set()
for i in range(len(falling_bytes)):
    corrupt_positions.add(falling_bytes[i])
    distances = graph.flood_fill({Pos(0, 0)}, neighbours)
    if end_pos not in distances:
        print(f"Part 2: {falling_bytes[i].col},{falling_bytes[i].row}")
        break
