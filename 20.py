from grid import Grid, NESW, Pos
import graph

lines = open("20_input.txt", "r").read().splitlines()
grid = Grid.create(lines)


def neighbours(pos: Pos) -> list[Pos]:
    return [n for n in pos.neighbours(NESW.DIRS) if n.at(lines) != "#"]


start_pos = [pos for pos in grid.positions() if pos.at(lines) == "S"][0]
end_pos = [pos for pos in grid.positions() if pos.at(lines) == "E"][0]

distances: dict[Pos, int] = graph.flood_fill({start_pos}, neighbours)
path: list[Pos] = graph.get_floodfill_path(end_pos, distances, neighbours)

part1 = 0
part2 = 0
for i in range(len(path)):
    for j in range(i + 100, len(path)):
        m = path[i].manhattan(path[j])
        if m == 2 and m + 100 <= j - i:
            part1 += 1
        if m <= 20 and m + 100 <= j - i:
            part2 += 1
print("Part 1:", part1)
print("Part 2:", part2)
