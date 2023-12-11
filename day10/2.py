import sys
from typing import List

"""
– | is a vertical pipe connecting above and below.
– ─ is a horizontal pipe connecting right and left.
– └ is a 90─degree bend connecting above and right.
– ┘ is a 90─degree bend connecting above and left. 
– ┐ is a 90─degree bend connecting below and left.
– ┌ is a 90─degree bend connecting below and right.
– . is ground; there is no pipe in this tile.
– S is the starting position of the animal; there is a pipe on this tile, but sketch doesn't show the pipe's shape.
"""

MATRIX = []


def get_next_pipe(path, point):
    if not len(path):
        path.append(point)
        down = get_next_pipe(path, go_down(point))
        if down:
            return down
        right = get_next_pipe(path, go_right(point))
        if right:
            return right
        left = get_next_pipe(path, go_left(point))
        if left:
            return left
        up = get_next_pipe(path, go_up(point))
        if up:
            return up
    prev_point = path[-1]
    path.append(point)
    prev_x, prev_y = prev_point
    x, y = point
    match MATRIX[y][x]:
        case 'S':
            return path
        case '|':
            if prev_x < x or prev_x > x:
                return None
            if prev_y < y:
                return get_next_pipe(path, go_down(point))
            return get_next_pipe(path, go_up(point))
        case '─':
            if prev_y < y or prev_y > y:
                return None
            if prev_x < x:
                return get_next_pipe(path, go_right(point))
            return get_next_pipe(path, go_left(point))
        case '└':
            if prev_x < x or prev_y > y:
                return None
            if prev_x > x:
                return get_next_pipe(path, go_up(point))
            return get_next_pipe(path, go_right(point))
        case '┘':
            if prev_x > x or prev_y > y:
                return None
            if prev_y < y:
                return get_next_pipe(path, go_left(point))
            return get_next_pipe(path, go_up(point))
        case '┐':
            if prev_x > x or prev_y < y:
                return None
            if prev_x < x:
                return get_next_pipe(path, go_down(point))
            return get_next_pipe(path, go_left(point))
        case '┌':
            if prev_x < x or prev_y < y:
                return None
            if prev_y > y:
                return get_next_pipe(path, go_right(point))
            return get_next_pipe(path, go_down(point))
        case _:
            return None


def go_up(p):
    x, y = p[0], p[1] - 1
    if y < 0:
        return None
    return [x, y]


def go_right(p):
    x, y = p[0] + 1, p[1]
    if x >= len(MATRIX[0]):
        return None
    return [x, y]


def go_down(p):
    x, y = p[0], p[1] + 1
    if y >= len(MATRIX):
        return None
    return [x, y]


def go_left(p):
    x, y = p[0] - 1, p[1]
    if x < 0:
        return None
    return [x, y]


def get_interior_points(path: list[int]) -> List[List[int]]:
    interior_points = []
    for idx in range(len(path) - 1):
        x, y = path[idx]
        next_x, next_y = path[idx + 1]
        go = lambda p: p
        # Always go clockwise
        if next_x == x + 1:
            go = go_down
        elif next_x == x - 1:
            go = go_up
        elif next_y < y:
            go = go_right
        elif next_y > y:
            go = go_left
        else:
            print(x, y, next_x, next_y)

        for [point_x, point_y] in ([x, y], [next_x, next_y]):
            # Check this point and the next for this direction.
            for _ in range(len(MATRIX[0])):
                point = go([point_x, point_y])
                if not point:
                    print(f"Hit the edge of the grid after {point_x}, {point_y}, reversing path")
                    raise ValueError("Hit the edge of the grid")
                point_x, point_y = point
                if [point_x, point_y] in path:
                    # Hit pipe boundary
                    break
                if [point_x, point_y] not in interior_points:
                    # print(f"Found an interior point {MATRIX[poss_y][poss_x]} at {poss_x}, {poss_y}")
                    interior_points.append([point_x, point_y])
    return interior_points


def parse_input(f):
    start = []
    for i, line in enumerate(f):
        line = line.strip()
        char_list = []
        for j, char in enumerate(line):
            char_list.append(char)
            if char == 'S':
                start = [j, i]

        MATRIX.append(char_list)
    return start


def main():
    with open('input10.txt', encoding='utf-8') as f:
        # print(f"Vertical step offset: {vertical_step_offset}")
        start = parse_input(f)
        print(f"START {start}")
        path = get_next_pipe([], start)
        # part_1 = len(path) // 2
        # print(f"Part 1: {part_1}")
        try:
            interior_points = get_interior_points(path)
        except ValueError:
            path.reverse()
            interior_points = get_interior_points(path)
        print(f"Part 2: {len(interior_points)}")


if __name__ == '__main__':
    sys.setrecursionlimit(15000)
    main()
