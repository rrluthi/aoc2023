from typing import Optional, Self
from dataclasses import dataclass


@dataclass
class Coordinate:
    row: int
    position: int

    def __add__(self, value: Self) -> Self:
        return Coordinate(self.row + value.row, self.position + value.position)

    def __sub__(self, value: Self) -> Self:
        return Coordinate(self.row - value.row, self.position - value.position)

    def __eq__(self, value: Self) -> bool:
        return self.row == value.row and self.position == value.position


def check_for_reflection(index: int, rows: list[str], fix_smudge: bool = False) -> (bool, Optional[Coordinate]):
    current_row = index
    reflection = False
    smudge_replaced = None  # Only one smudge can be fixed per map.

    for i in range(index + 1):
        if len(rows) > current_row + i + 1:
            this_row = rows[current_row - i]
            next_row = rows[current_row + i + 1]

            if this_row != next_row:
                if fix_smudge and not smudge_replaced:
                    diff = []
                    for index, (a, b) in enumerate(zip(this_row, next_row)):
                        if a != b:
                            diff.append(index)
                    if len(diff) == 1:
                        smudge_replaced = Coordinate(current_row - i, diff[0])
                        reflection = True
                        continue

                return False, None

            reflection = True

    return reflection, smudge_replaced if reflection else None


def find_reflections(rows: list[str], allow_smudges: bool = False) -> list[int]:
    reflections = []
    for index in range(len(rows)):
        reflection, smudge = check_for_reflection(index, rows, allow_smudges)
        if smudge and allow_smudges:
            allow_smudges = False
            rows[smudge.row] = (
                rows[smudge.row][:smudge.position]
                + ("." if rows[smudge.row][smudge.position] == "#" else "#")
                + rows[smudge.row][smudge.position+1:]
            )  # Replace smudged mirror in map.
        if reflection and not allow_smudges:
            reflections.append(index)

    return reflections


def find_pattern_reflections(pattern: str, allow_smudges: bool = False) -> (list[int], list[int]):
    rows = pattern.splitlines()
    horizontal_reflections = find_reflections(rows, allow_smudges)
    columns = list("".join(row) for row in zip(*rows))
    vertical_reflections = find_reflections(columns, allow_smudges)
    if allow_smudges:
        print(f"{horizontal_reflections=}, {vertical_reflections=}")
    return horizontal_reflections, vertical_reflections


def calculate_total_reflections(patterns: list[str]) -> int:
    total = 0
    for pattern in patterns:
        horizontal, vertical = find_pattern_reflections(pattern)
        horizontal_smudged, vertical_smudged = find_pattern_reflections(pattern, True)
        horizontal_diffs = set(horizontal_smudged) - set(horizontal)
        vertical_diffs = set(vertical_smudged) - set(vertical)

        horizontal_sum = sum((reflection + 1) * 100 for reflection in horizontal_diffs)
        vertical_sum = sum(reflection + 1 for reflection in vertical_diffs)
        total += horizontal_sum + vertical_sum

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
