from dataclasses import dataclass
import sys
from typing import List


@dataclass
class Mapping:
    source_start: int
    dest_start: int
    length: int


@dataclass
class Map:
    name: str
    mappings: List[Mapping]


@dataclass
class MapResult:
    name: str
    value: int


@dataclass
class Seed:
    start: int
    end: int
    steps: List[MapResult]


def apply_mapping(seed: Seed, maps: List[Map], lowest) -> int:
    if len(seed.steps) == len(maps):
        if seed.start < lowest:
            lowest = seed.start
            print(seed)
        return lowest

    curr_map = maps[len(seed.steps)]

    for mapping in curr_map.mappings:

        if seed.start < mapping.source_start < seed.end:
            low_seed = Seed(start=seed.start, end=mapping.source_start, steps=seed.steps.copy())
            # print("LOW SEED", low_seed)
            lowest = apply_mapping(low_seed, maps, lowest)
            seed.start = mapping.source_start

        if mapping.source_start > seed.end > mapping.source_start + mapping.length - 1:
            high_seed = Seed(start=mapping.source_start + mapping.length - 1, end=seed.end, steps=seed.steps.copy())
            # print("HIGH SEED", high_seed)
            lowest = apply_mapping(high_seed, maps, lowest)
            seed.start = mapping.source_start + mapping.length - 1

        if mapping.source_start <= seed.start <= mapping.source_start + mapping.length - 1:
            seed.start += mapping.dest_start - mapping.source_start
            seed.end += mapping.dest_start - mapping.source_start
            break

    seed.steps.append(MapResult(curr_map.name, seed.start))
    return apply_mapping(seed, maps, lowest)


def get_lowest_location(seeds: List[Seed], maps: List[Map]) -> int:
    lowest = sys.maxsize
    for seed in seeds:
        potential_lowest = apply_mapping(seed, maps, lowest)
        if potential_lowest < lowest:
            lowest = potential_lowest
    return lowest


def parse_step(step: str) -> Map:
    step = step.strip()
    name, mappings = step.split(' map:')
    mappings = mappings.strip().split('\n')
    mappings = [m.strip().split(' ') for m in mappings]
    mappings = [Mapping(dest_start=int(t[0]), source_start=int(t[1]), length=int(t[2])) for t in mappings]
    return Map(name, mappings)


def parse_seeds(seeds: str) -> List[Seed]:
    seed_numbers = [int(s) for s in seeds.split(' ')]
    seeds = []
    while seed_numbers:
        seed_start = seed_numbers.pop(0)
        length = seed_numbers.pop(0)
        seeds.append(Seed(start=seed_start, end=seed_start + length, steps=[]))
    return seeds


def parse_input(f) -> (List[Seed], List[Map]):
    seeds = []
    maps = []
    step = ''
    for line in f:
        line = line.strip()
        if line.startswith('seeds:'):
            seeds = parse_seeds(line.split('seeds: ')[1])
        elif not line.strip():
            if step:
                maps.append(step)
            step = ''
        else:
            step += line + '\n'
    maps.append(step)
    maps = [parse_step(m) for m in maps]
    return seeds, maps


def main():
    with open('../day6/input6.txt') as f:
        seeds, mappings = parse_input(f)
        score = get_lowest_location(seeds, mappings)
        print(score)


if __name__ == "__main__":
    main()