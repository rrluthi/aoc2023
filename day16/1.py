from enum import Enum
from dataclasses import dataclass
from typing import List
import sys


class Direction(Enum):
    UP = 'up'
    DOWN = 'down'
    LEFT = 'left'
    RIGHT = 'right'


class Beam:
    direction: Direction | None = None

    def __init__(self, direction: Direction):
        self.direction = direction

    def __eq__(self, other) -> bool:
        return self.direction == other.direction

    def __repr__(self):
        return f"Beam({self.direction})"


class TileType(Enum):
    EMPTY = '.'
    SPLIT_H = '-'
    SPLIT_V = '|'
    MIRROR_A = '/'
    MIRROR_B = "\\"

    def __str__(self):
        return self.value


class Tile:
    type: TileType
    beams: List[Beam]
    energized: bool = False

    def __init__(self, c):
        self.type = TileType(c)
        self.beams = []

    def __repr__(self):
        return f"{'*' if self.energized else self.type}"


def beam_continue(grid, x, y, beam):
    match beam.direction:
        case Direction.UP:
            beam_up(grid, x, y)
        case Direction.DOWN:
            beam_down(grid, x, y)
        case Direction.LEFT:
            beam_left(grid, x, y)
        case Direction.RIGHT:
            beam_right(grid, x, y)


def beam_right(grid, x, y):
    if x + 1 < len(grid[y]):
        energize(grid, x + 1, y, Beam(Direction.RIGHT))


def beam_left(grid, x, y):
    if x - 1 >= 0:
        energize(grid, x - 1, y, Beam(Direction.LEFT))


def beam_up(grid, x, y):
    if y - 1 >= 0:
        energize(grid, x, y - 1, Beam(Direction.UP))


def beam_down(grid, x, y):
    if y + 1 < len(grid):
        energize(grid, x, y + 1, Beam(Direction.DOWN))


def energize(grid, x, y, beam):
    current_tile = grid[y][x]
    current_tile.energized = True
    if beam in current_tile.beams:
        return
    current_tile.beams.append(beam)

    match current_tile.type:
        case TileType.EMPTY:
            beam_continue(grid, x, y, beam)
        case TileType.SPLIT_H:  # -
            if beam.direction in [Direction.UP, Direction.DOWN]:
                beam_left(grid, x, y)
                beam_right(grid, x, y)
            elif beam.direction in [Direction.LEFT, Direction.RIGHT]:
                beam_continue(grid, x, y, beam)
        case TileType.SPLIT_V:  # |
            if beam.direction in [Direction.UP, Direction.DOWN]:
                beam_continue(grid, x, y, beam)
            elif beam.direction in [Direction.LEFT, Direction.RIGHT]:
                beam_up(grid, x, y)
                beam_down(grid, x, y)
        case TileType.MIRROR_A:  # /
            match beam.direction:
                case Direction.UP: 
                    beam_right(grid, x, y)
                case Direction.DOWN:
                    beam_left(grid, x, y)
                case Direction.LEFT:
                    beam_down(grid, x, y)
                case Direction.RIGHT:
                    beam_up(grid, x, y)
        case TileType.MIRROR_B:  # \
            match beam.direction:
                case Direction.UP:
                    beam_left(grid, x, y)
                case Direction.DOWN:
                    beam_right(grid, x, y)
                case Direction.LEFT:
                    beam_up(grid, x, y)
                case Direction.RIGHT:
                    beam_down(grid, x, y)


def parse_input(f):
    lines = f.readlines()
    grid = []
    for line in lines:
        grid.append([Tile(c) for c in line.strip()])
    return grid


def main():
    with open("input16.txt") as f:
        grid = parse_input(f)
    energize(grid, 0, 0, Beam(Direction.RIGHT))
    print(sum([sum([1 for tile in row if tile.energized]) for row in grid]))


if __name__ == "__main__":
    sys.setrecursionlimit(15000)
    main()
