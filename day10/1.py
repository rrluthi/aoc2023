import sys
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
                return go_down(path)
            return go_up(path)
        case '─':
            if prev_y < y or prev_y > y:
                return None
            if prev_x < x:
                return go_right(path)
            return go_left(path)
        case '└':
            if prev_x < x or prev_y > y:
                return None
            if prev_x > x:
                return go_up(path)
            return go_right(path)
        case '┘':
            if prev_x > x or prev_y > y:
                return None
            if prev_y < y:
                return go_left(path)
            return go_up(path)
        case '┐':
            if prev_x > x or prev_y < y:
                return None
            if prev_x < x:
                return go_down(path)
            return go_left(path)
        case '┌':
            if prev_x < x or prev_y < y:
                return None
            if prev_y > y:
                return go_right(path)
            return go_down(path)
        case _:
            return None


def go_up(path):
    p = path[-1]
    # print("go_up", p)
    try:
        x, y = p[0], p[1] - 1
        next_point = MATRIX[y][x]
        return get_next_pipe(path, [x, y])
    except IndexError:
        return None


def go_right(path):
    p = path[-1]
    # print("go_right", p)
    try:
        x, y = p[0] + 1, p[1]
        next_point = MATRIX[y][x]
        return get_next_pipe(path, [x, y])
    except IndexError:
        return None


def go_down(path):
    p = path[-1]
    # print("go_down")
    try:
        x, y = p[0], p[1] + 1
        next_point = MATRIX[y][x]
        return get_next_pipe(path, [x, y])
    except IndexError:
        return None


def go_left(path):
    p = path[-1]
    # print("go_left", p)
    try:
        x, y = p[0] - 1, p[1]
        next_point = MATRIX[y][x]
        return get_next_pipe(path, [x, y])
    except IndexError:
        return None


def get_valid_paths(start):
    path = [start]
    # From start you can go left, right, up, down ... 2 paths should be valid (loops)
    left = go_left(path.copy())
    right = go_right(path.copy())
    up = go_up(path.copy())
    down = go_down(path.copy())
    return list(filter(lambda x: x is not None, [left, right, up, down]))


def find_meeting_point_distance(paths):
    assert len(paths) == 2
    path1, path2 = paths
    for i, (j, k) in enumerate(zip(path1, path2)):
        if i > 0 and k == j:
            return i
    return None


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
        start = parse_input(f)
        print(f"START {start}")
        valid_paths = get_valid_paths(start)
        meeting_point_distance = find_meeting_point_distance(valid_paths)
        print(meeting_point_distance)


if __name__ == '__main__':
    sys.setrecursionlimit(30000)
    main()
