from dataclasses import dataclass
from collections import OrderedDict
import re


lens_pattern = re.compile(r'^([^=-]*)([=-])([\d])?$')


@dataclass
class Lens:
    label: str
    box: int
    operator: str
    focal_length: int


def hash_step(value, step):
    if len(step) == 0:
        return value
    char_code = ord(step[0])
    value += char_code
    value *= 17
    value %= 256
    return hash_step(value, step[1:])


def build_lens_array(lenses):
    lens_array = {n: OrderedDict() for n in list(range(0, 256))}
    for lens in lenses:
        if lens.operator == '=':
            lens_array[lens.box][lens.label] = lens
        else:
            if lens.label in lens_array[lens.box]:
                del lens_array[lens.box][lens.label]
    return lens_array


def calculate_lens_array_strength(lens_array):
    lens_array_total = 0
    for box, lens_list in lens_array.items():
        box_total = 0
        m = box + 1
        for i, (label, lens) in enumerate(lens_list.items()):
            lens_power = m * (i+1) * lens.focal_length
            box_total += lens_power
        lens_array_total += box_total
    return lens_array_total


def parse_input(f):
    lenses = []
    for line in f:
        line = line.strip()
        steps = line.split(',')
        for step in steps:
            label, operator, focal_length = lens_pattern.match(step).groups()
            lenses.append(Lens(
                label=label,
                box=hash_step(0, label),
                operator=operator,
                focal_length=int(focal_length) if focal_length else None
            ))
    return lenses


def main():

    with open('input15.txt') as f:
        lenses = parse_input(f)
        lens_array = build_lens_array(lenses)
        lens_array_total = calculate_lens_array_strength(lens_array)
        print(lens_array_total)


if __name__ == "__main__":
    main()
