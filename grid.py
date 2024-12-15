from dataclasses import dataclass
import functools
from typing import Iterator, List


@dataclass(frozen=True, eq=True)
@functools.total_ordering
class Pos:
    """
    Row/column position in a 2-dimensional grid.
    """

    __slots__ = ("row", "col")

    row: int
    col: int

    def add(self, pos: "Pos") -> "Pos":
        return Pos.create(self.row + pos.row, self.col + pos.col)

    def subtract(self, pos: "Pos") -> "Pos":
        return Pos.create(self.row - pos.row, self.col - pos.col)

    def negate(self) -> "Pos":
        return Pos.create(-self.row, -self.col)

    def multiply(self, factor) -> "Pos":
        return Pos.create(factor * self.row, factor * self.col)

    def wrap(self, pos: "Pos") -> "Pos":
        return Pos.create(self.row % pos.row, self.col % pos.col)

    def at(self, lines: List[List]):
        """
        Returns the element at this position.
        """
        return lines[self.row][self.col]

    def neighbours(self, dirs: list["Pos"]) -> Iterator["Pos"]:
        """
        Generates neighbours of this position.
        """
        for dir in dirs:
            yield self.add(dir)

    def __add__(self, other):
        return Pos.create(self.row + other.row, self.col + other.col)

    def __sub__(self, other):
        return Pos.create(self.row - other.row, self.col - other.col)

    def __neg__(self):
        return Pos.create(-self.row, -self.col)

    def __mul__(self, other):
        return Pos.create(other * self.row, other * self.col)

    def __lt__(self, other):
        """
        Sorts on row, then col.
        """
        if self.row == other.row:
            return self.col < other.col
        return self.row < other.row

    @functools.cache
    def create(row, col) -> "Pos":
        return Pos(row, col)


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

    def positions(self) -> Iterator[Pos]:
        """
        Iterates over all positions on the grid, yields Pos objects.
        """
        for row in range(self.rows):
            for col in range(self.cols):
                yield Pos.create(row, col)

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
