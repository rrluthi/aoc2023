
def check_for_reflection(index: int, rows: list[str]) -> bool:
    current_row = index
    reflection = False

    for i in range(index + 1):
        if len(rows) > current_row + i + 1:
            this_row = rows[current_row - i]
            next_row = rows[current_row + i + 1]
            if this_row != next_row:
                return False

            reflection = True

    return reflection


def find_reflections(rows: list[str]) -> list[int]:
    reflections = []
    for index in range(len(rows)):
        reflection = check_for_reflection(index, rows)
        if reflection:
            reflections.append(index)

    return reflections


def find_pattern_reflections(pattern: str) -> (list[int], list[int]):
    rows = pattern.splitlines()
    horizontal_reflections = find_reflections(rows)
    columns = list("".join(row) for row in zip(*rows))
    vertical_reflections = find_reflections(columns)
    print(f"{horizontal_reflections=}, {vertical_reflections=}")
    return horizontal_reflections, vertical_reflections


def calculate_total_reflections(patterns: list[str]) -> int:
    total = 0
    for pattern in patterns:
        horizontal, vertical = find_pattern_reflections(pattern)
        vertical_sum = sum(reflection + 1 for reflection in vertical)
        horizontal_sum = sum((reflection + 1) * 100 for reflection in horizontal)
        total += vertical_sum + horizontal_sum

    return total


def parse_input(f):
    valley = f.read()
    patterns = valley.split("\n\n")
    return patterns


def main():
    with open('input13.txt') as file:
        patterns = parse_input(file)

    total = calculate_total_reflections(patterns)
    print(total)


if __name__ == "__main__":
    main()
