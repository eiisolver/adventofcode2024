from dataclasses import dataclass
from typing import List


@dataclass(frozen=True, eq=True)
class Pos:
    """
    Row/column position in a 2-dimensional grid.
    """

    row: int
    col: int

    def add(self, pos: "Pos") -> "Pos":
        return Pos(self.row + pos.row, self.col + pos.col)

    def subtract(self, pos: "Pos") -> "Pos":
        return Pos(self.row - pos.row, self.col - pos.col)

    def negate(self) -> "Pos":
        return Pos(-self.row, -self.col)

    def at(self, lines: List[List]):
        """
        Returns the element at this position.
        """
        return lines[self.row][self.col]


@dataclass
class Grid:
    """
    Some useful methods for working with a 2-dimensional grid.
    Note: contains only the size of the grid, does not own the actual data.
    """

    rows: int
    cols: int

    def contains(self, pos: Pos) -> bool:
        """
        Checks if the given position is on the grid.
        """
        return 0 <= pos.row < self.rows and 0 <= pos.col < self.cols

    def rows_cols(self):
        """
        Iterates for all rows/columns, yields Pos objects.
        """
        for row in range(self.rows):
            for col in range(self.cols):
                yield Pos(row, col)

    def walk(self, start: Pos, delta: Pos, include_start: bool = False):
        """
        Generator that yields positions, walking from start, until leaving the grid.
        """
        if include_start:
            yield start
        curr_pos = start.add(delta)
        while self.contains(curr_pos):
            yield curr_pos
            curr_pos = curr_pos.add(delta)

    @classmethod
    def create(cls, list) -> "Grid":
        return Grid(len(list), len(list[0]))


class NESW:
    """
    North/east/south/west directions.
    """

    N = Pos(-1, 0)
    E = Pos(0, 1)
    S = Pos(1, 0)
    W = Pos(0, -1)
    DIRS = [N, E, S, W]
