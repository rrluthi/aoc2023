from typing import Optional, Self
from dataclasses import dataclass


@dataclass(frozen=True, eq=True)
class Coordinate:
    """Single cordinate."""

    row: int
    position: int

    def __add__(self, __value: Self) -> Self:
        return Coordinate(self.row + __value.row, self.position + __value.position)

    def __sub__(self, __value: Self) -> Self:
        return Coordinate(self.row - __value.row, self.position - __value.position)

    def __eq__(self, __value: Self) -> bool:
        return self.row == __value.row and self.position == __value.position


def check_for_reflection(
    index: int, rows: list[str], fix_smudge: bool = False
) -> tuple[bool, Optional[Coordinate]]:
    """Check for reflection in a given row."""
    current_row = index
    reflection = False
    smudge_replaced = None  # Only one smudge can be fixed per map.

    for i in range(index + 1):
        try:
            this_row = rows[current_row - i]
            next_row = rows[current_row + i + 1]
        except IndexError:
            break  # In case of final rows.

        if this_row != next_row:
            if fix_smudge and not smudge_replaced:
                diff = [index for index, (a, b) in enumerate(zip(this_row, next_row)) if a != b]
                if len(diff) == 1:
                    smudge_replaced = Coordinate(current_row - i, diff[0])
                    reflection = True
                    continue

            return False, None

        reflection = True

    return reflection, smudge_replaced if reflection else None


def find_reflections(
    rows: list[str], allow_smudges: bool = False
) -> tuple[list[int], list[str]]:
    reflections = []
    for index in range(len(rows)):
        reflection, smudge = check_for_reflection(index, rows, allow_smudges)
        if smudge and allow_smudges:
            allow_smudges = False
            rows[smudge.row] = (
                rows[smudge.row][: smudge.position]
                + ("." if rows[smudge.row][smudge.position] == "#" else "#")
                + rows[smudge.row][smudge.position + 1 :]
            )  # Replace smudged mirror in map.
        if reflection and not allow_smudges:
            reflections.append(index)

    return reflections, rows


def find_total_reflections(pattern: str, allow_smudges: bool = False) -> tuple[list[int], list[int]]:
    rows = pattern.splitlines()
    horizontal_reflections, rows = find_reflections(rows, allow_smudges)
    columns = list("".join(row) for row in zip(*rows))
    vertical_reflections, _ = find_reflections(columns, allow_smudges)

    return horizontal_reflections, vertical_reflections

def main():
    with open('input13.txt') as file:
        valley_map = file.read()
        patterns = valley_map.split("\n\n")

        total = 0
        for pattern in patterns:
            horizontal, vertical = find_total_reflections(pattern, False)

            total += sum(reflection + 1 for reflection in vertical) + sum(
                (reflection + 1) * 100 for reflection in horizontal
            )

    return print(total)


if __name__ == "__main__":
    main()
