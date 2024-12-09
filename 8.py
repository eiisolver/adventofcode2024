from collections import defaultdict
import itertools
from grid import Grid

lines = open("8_input.txt", "r").read().splitlines()
grid = Grid.create(lines)

# Map from frequency to list of positions.
all_antennas = defaultdict(list)
for pos in grid.rows_cols():
    freq = pos.at(lines)
    if freq != ".":
        all_antennas[freq].append(pos)
antinodes = set()
for freq, positions in all_antennas.items():
    for pos1, pos2 in itertools.combinations(positions, 2):
        delta = pos1.subtract(pos2)
        antinodes.add(pos1.add(delta))
        antinodes.add(pos2.subtract(delta))
print("Part 1:", len([n for n in antinodes if grid.contains(n)]))

antinodes2 = set()
for freq, positions in all_antennas.items():
    for pos1, pos2 in itertools.combinations(positions, 2):
        delta = pos1.subtract(pos2)
        for n in grid.walk(pos2, delta):
            antinodes2.add(n)
        for n in grid.walk(pos1, delta.negate()):
            antinodes2.add(n)
print("Part 2:", len([n for n in antinodes2 if grid.contains(n)]))
