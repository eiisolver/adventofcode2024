from grid import Grid, NESW, Pos

lines = open("12_input.txt", "r").read().splitlines()
grid = Grid.create(lines)


def expand(region: set[Pos], positions: set[Pos]) -> set[Pos]:
    """
    Returns the set of positions that belong to the same region.
    """
    result = set()
    for pos in positions:
        for pos2 in pos.neighbours(NESW.DIRS):
            if grid.contains(pos2) and pos2.at(lines) == pos.at(lines) and pos2 not in region:
                result.add(pos2)
    return result


def perimeter(region: set[Pos]) -> int:
    result = 0
    for pos in region:
        for pos2 in pos.neighbours(NESW.DIRS):
            if pos2 not in region:
                result += 1
    return result


def sides(region: set[Pos]) -> int:
    sorted_positions = sorted([p for p in region])
    sides = 0
    for d in range(4):
        dir1 = NESW.DIRS[d]  # Side to check
        dir2 = NESW.E if d % 2 == 0 else NESW.S  # Direction to walk to expand the side
        visited = set()
        for pos in sorted_positions:
            if pos in visited:
                continue
            visited.add(pos)
            if pos.add(dir1) in region:
                continue
            sides += 1
            # New side detected, expand the side
            for next_pos in grid.walk(pos, dir2):
                if not next_pos in region:
                    break
                visited.add(next_pos)
                if next_pos.add(dir1) in region:
                    break
    return sides


region_list: list[set[Pos]] = []  # List of regions
visited = set()  # All positions that have been added to a region
for pos in grid.positions():
    if pos not in visited:
        # New region
        added_positions = {pos}
        curr_region = {pos}
        while added_positions:
            added_positions = expand(curr_region, added_positions)
            curr_region |= added_positions
        visited |= curr_region
        region_list.append(curr_region)


part1 = sum(len(region) * perimeter(region) for region in region_list)
print("Part 1:", part1)
part2 = sum(len(region) * sides(region) for region in region_list)
print("Part 2:", part2)
