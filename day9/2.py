from typing import List
from dataclasses import dataclass


@dataclass
class Sequence:
    value: List[int]
    steps: List[List[int]]
    prev_value: int
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


def calc_history(steps: List[List[int]], prev_val, next_val) -> (int, int):
    if len(steps) == 1:
        return steps[0][0] - prev_val, steps[0][-1] + next_val
    else:
        return calc_history(steps[:-1], steps[-1][0] - prev_val, steps[-1][-1] + next_val)


def parse_input(f) -> List[Sequence]:
    sequences = []
    for line in f:
        numbers = [int(n) for n in line.strip().split(' ')]
        steps = build_steps([numbers])
        prev_value, next_val = calc_history(steps, 0, 0)
        sequences.append(Sequence(numbers, steps, prev_value, next_val))
    return sequences


def main():
    with open('input9.txt') as f:
        sequences = parse_input(f)
        sum_prev_values = sum([s.prev_value for s in sequences])
        print(sum_prev_values)
        return sum_prev_values


if __name__ == "__main__":
    main()
