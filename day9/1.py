from typing import List
from dataclasses import dataclass


@dataclass
class Sequence:
    value: List[int]
    steps: List[List[int]]
    next_value: int


def build_steps(steps: List[List[int]]) -> List[List[int]]:
    curr_step = steps[-1]
    step = []
    for i, num in enumerate(curr_step[0:len(curr_step)-1]):
        step.append(curr_step[i+1] - num)
    if all([step[i] == 0 for i in range(len(step)-1)]):
        steps.append(step)
        return steps
    else:
        steps.append(step)
        return build_steps(steps)


def calc_next_value(steps: List[List[int]], val):
    if len(steps) == 1:
        return val + steps[-1][-1]
    else:
        return calc_next_value(steps[:-1], val + steps[-1][-1])


def parse_input(f) -> List[Sequence]:
    sequences = []
    for line in f:
        numbers = [int(n) for n in line.strip().split(' ')]
        steps = build_steps([numbers])
        next_value = calc_next_value(steps, 0)
        sequences.append(Sequence(numbers, steps, next_value))
    return sequences


def main():
    with open('input9.txt') as f:
        sequences = parse_input(f)
        sum_next_values = sum([s.next_value for s in sequences])
        print(sum_next_values)
        return sum_next_values


if __name__ == "__main__":
    main()
