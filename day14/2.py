from enum import Enum
from typing import List
from itertools import starmap


class Tile(Enum):
    ROUND = 'O'
    CUBE = '#'
    EMPTY = '.'

    def __repr__(self):
        return self.value


def slide_north(grid: List[List[Tile]]):
    for col in range(len(grid[0])):
        empty_or_round_row = 0
        for row in range(len(grid)):
            current_tile = grid[row][col]
            match current_tile:
                case Tile.CUBE:
                    empty_or_round_row = row + 1
                case Tile.ROUND:
                    swap = grid[empty_or_round_row][col]
                    grid[empty_or_round_row][col] = current_tile
                    grid[row][col] = swap
                    empty_or_round_row += 1
                case Tile.EMPTY:
                    pass


def rotate_clockwise(grid: List[List[Tile]]):
    # rotate matrix 90 degrees clockwise
    return [list(row) for row in zip(*grid[::-1])]


def cycle(grid: List[List[Tile]]):
    for _ in range(4):
        slide_north(grid)
        grid = rotate_clockwise(grid)
    return grid


def round_rocks(row: List):
    return list(filter(lambda tile: tile == Tile.ROUND, row))


def calculate_weight(grid: List[List[Tile]]) -> int:
    reversed_grid = list(reversed(grid))
    return sum(starmap(lambda i, row: (i + 1) * len(round_rocks(row)), enumerate(reversed_grid)))


def parse_input(f):
    grid = []
    for line in f:
        grid.append([Tile(char) for char in line.strip()])
    return grid


def main():
    with open('sample14.txt') as file:
        grid = parse_input(file)
        seen = [grid]
        while True:
            grid = cycle(grid)
            if grid in seen:
                index = seen.index(grid)
                cycle_length = len(seen) - index
                final_index = index + (1000_000_000 - index) % cycle_length
                print(f"Cycle length: {cycle_length}")
                break
            seen.append(grid)

        weight = calculate_weight(seen[final_index])
        print(weight)


if __name__ == "__main__":
    main()
