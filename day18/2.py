from dataclasses import dataclass


directions = {
    '0': (1, 0),
    '1': (0, 1),
    '2': (-1, 0),
    '3': (0, -1),
}


@dataclass
class Instruction:
    direction: tuple
    value: int
    color: str


def build_trench(data):
    start = (0, 0)
    trench = [start]
    length = 0
    for i in data:
        end = tuple(a + i.value * b for a, b in zip(start, i.direction))
        length += i.value
        trench.append(end)
        start = end
    return trench, length


def draw_trench(trench):
    max_x = max(trench, key=lambda x: x[1])[1]
    max_y = max(trench, key=lambda x: x[0])[0]
    grid = [['.' for _ in range(max_y + 1)] for _ in range(max_x + 1)]
    current = trench.pop(0)
    while len(trench):
        next = trench.pop(0)
        if current[0] == next[0]:
            for y in range(min(current[1], next[1]), max(current[1], next[1]) + 1):
                grid[y][current[0]] = '#'
        else:
            for x in range(min(current[0], next[0]), max(current[0], next[0]) + 1):
                grid[current[1]][x] = '#'
        current = next
    for row in grid:
        print(''.join(row))


def calculate_area(trench, length):
    """
    Shoelace formula for calculating area of a polygon
    Pick's theorem for calculating area of a polygon with integer coordinates
    """
    r = 0
    for i in range(len(trench) - 1):
        y1, x1 = trench[i]
        y2, x2 = trench[i + 1]
        r += x1 * y2 - x2 * y1

    return abs(r) // 2 + length // 2 + 1


def parse_input(f):
    data = []
    for line in f:
        line = line.strip()
        d, value, rest = line.split(' ')
        color = rest.strip('(#)')
        value = int(color[0:5], 16)
        d = color[5:]
        instruction = Instruction(directions[d], int(value), color)
        data.append(instruction)
    return data


def main():
    with open('input18.txt') as f:
        data = parse_input(f)
    trench, length = build_trench(data)
    area = calculate_area(trench, length)

    print(area)


if __name__ == "__main__":
    main()
