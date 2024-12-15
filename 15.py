from typing import Optional
from grid import Grid, NESW, Pos

dir_map = {"^": NESW.N, ">": NESW.E, "v": NESW.S, "<": NESW.W}
lines = open("15_input.txt", "r").read().splitlines()
empty_index = lines.index("")
map = [line for line in lines[0:empty_index]]
grid = Grid.create(map)

directions = [dir_map[d] for line in lines[empty_index+1:] for d in line]
boxes: set[Pos] = set(pos for pos in grid.positions() if pos.at(map) == "O")
robot = [pos for pos in grid.positions() if pos.at(map) == "@"][0]

def move_box(pos: Pos, dir: Pos) -> bool:
    """
    Moves any box at this position.
    Returns true if a robot or box can be moved to this position.
    """
    if pos.at(map) == "#":
        return False
    if pos not in boxes:
        return True
    pos2 = pos.add(dir)
    result = move_box(pos2, dir)
    if result:
        boxes.add(pos2)
        boxes.remove(pos)
    return result

for dir in directions:
    next_pos = robot.add(dir)
    if move_box(next_pos, dir):
        robot = next_pos

print("Part 1:", sum(100*box.row + box.col for box in boxes))

# Part 2
boxes: set[Pos] = set(Pos(pos.row, 2*pos.col) for pos in grid.positions() if pos.at(map) == "O")
robot = [Pos(pos.row, 2*pos.col) for pos in grid.positions() if pos.at(map) == "@"][0]

def get_boxes(positions: set[Pos]) -> set[Pos]:
    """
    Returns set of wide boxes at the given positions.
    """
    result = set()
    for pos in positions:
        if pos in boxes:
            result.add(pos)
        west = pos.add(NESW.W)
        if west in boxes:
            result.add(west)
    return result

def move_wide_boxes(positions: set[Pos], dir: Pos) -> bool:
    """
    Moves all wide boxes at the given positions.
    Returns true if boxes/robot can be moved to these positions.
    """
    if any(map[pos.row][pos.col // 2] == "#" for pos in positions):
        return False
    # Get the boxes at these positions
    box_set = get_boxes(positions)
    if not box_set:
        # No boxes here, ok to move to here.
        return True
    # Calculate the positions that these boxes will occupy after moving
    if dir == NESW.E:
        positions2 = set(pos.add(Pos(0, 2)) for pos in box_set)
    else:
        positions2 = set(pos.add(dir) for pos in box_set)
        if dir in (NESW.N, NESW.S):
            positions2 |=  set(pos.add(NESW.E).add(dir) for pos in box_set)
    # Check if the boxes can move here
    result = move_wide_boxes(positions2, dir)
    if result:
        # Yes, move, the boxes
        for box in box_set:
            boxes.add(box.add(dir))
            boxes.remove(box)
    return result

for dir in directions:
    next_pos = robot.add(dir)
    if move_wide_boxes({next_pos}, dir):
        robot = next_pos

print("Part 2:", sum(100*box.row + box.col for box in boxes))
