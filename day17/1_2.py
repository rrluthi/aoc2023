from p_queue import PriorityQ
from enum import Enum
from dataclasses import dataclass
from typing import NamedTuple, List


class Point(NamedTuple):
    x: int
    y: int


class Direction(Enum):
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    UP = (0, -1)
    DOWN = (0, 1)
    BLANK = (0, 0)


opposites = {
    Direction.LEFT: Direction.RIGHT,
    Direction.RIGHT: Direction.LEFT,
    Direction.UP: Direction.DOWN,
    Direction.DOWN: Direction.UP,
    Direction.BLANK: None
}


@dataclass
class Block:
    pos: Point
    direction: Direction
    repeat: int

    def __hash__(self):
        return hash(((self.pos.x, self.pos.y), self.direction, self.repeat))


def find_min(grid: List[List[int]], min_steps: int, max_steps:int):
    queue = PriorityQ()
    start = Block(Point(0, 0), Direction.BLANK, 0)
    queue.add_task(start, 0)
    w = len(grid[0])
    h = len(grid)
    seen = {}
    while True:
        try:
            current_block, value = queue.pop_task()
            (x, y), last_move, repeat = current_block.pos, current_block.direction, current_block.repeat
        except KeyError as err:
            print(err)
            break
        if (x, y, last_move, repeat) in seen:
            continue
        else:
            seen[(x, y, last_move, repeat)] = value
        moves = [d for d in Direction if d != Direction.BLANK]
        if repeat < min_steps and last_move != Direction.BLANK:
            moves = [last_move]
        opposite = opposites[last_move]
        for move in moves:
            if move == opposite:
                continue
            if move == last_move:
                if repeat == max_steps:
                    continue
                next_repeat = repeat + 1
            else:
                next_repeat = 1
            dx, dy = move.value
            next_x = x + dx
            next_y = y + dy
            if not (0 <= next_x < w and 0 <= next_y < h):
                continue
            if (next_x, next_y, move, next_repeat) in seen:
                continue
            next_value = value + grid[next_y][next_x]
            if next_x == w - 1 and next_y == h - 1:
                if min_steps <= next_repeat:
                    return next_value
                continue
            next_block = Block(Point(next_x, next_y), move, next_repeat)
            queue.add_task(next_block, next_value)


def parse_input(f):
    grid = []
    for line in f:
        line = line.strip()
        grid.append([int(c) for c in line])
    return grid


def main():
    with open("input17.txt") as f:
        grid = parse_input(f)
        total_1 = find_min(grid, 1, 3)
        print(f"Part 1: {total_1}")
        total_2 = find_min(grid, 4, 10)
        print(f"Part 2: {total_2}")


if __name__ == "__main__":
    main()
