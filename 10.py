from grid import Grid, NESW, Pos

lines = open("10_input.txt", "r").read().splitlines()
grid = Grid.create(lines)
topo_map = []
for line in lines:
    topo_map.append([int(x) for x in line])


def expand(positions: dict[Pos, int]) -> dict[Pos, int]:
    """
    Returns the set of next-higher positions.
    Maps are from position -> number of paths to that position.
    """
    result = dict()
    for pos in positions:
        for pos2 in pos.neighbours(NESW.DIRS):
            if grid.contains(pos2) and pos2.at(topo_map) == pos.at(topo_map) + 1:
                result[pos2] = positions[pos] + result.get(pos2, 0)
    return result


part1 = 0
part2 = 0
for pos in grid.positions():
    if pos.at(topo_map) == 0:
        # Potential trail head
        positions = {pos: 1}
        for _ in range(9):
            positions = expand(positions)
        part1 += len(positions)
        part2 += sum(positions.values())

print("Part 1:", part1)
print("Part 2:", part2)
