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
    value: int
    steps: List[MapResult]


def apply_mapping(seed: Seed, next_map: Map) -> Seed:
    for mapping in next_map.mappings:
        if mapping.source_start <= seed.value < mapping.source_start + mapping.length:
            seed.value += mapping.dest_start - mapping.source_start
            break
    seed.steps.append(MapResult(next_map.name, seed.value))
    return seed


def get_lowest_location(seeds: List[Seed], maps: List[Map]) -> int:
    lowest = sys.maxsize
    for seed in seeds:
        for next_map in maps:
            apply_mapping(seed, next_map)
        if seed.value < lowest:
            lowest = seed.value
    return lowest


def parse_step(step: str) -> Map:
    step = step.strip()
    name, mappings = step.split(' map:')
    mappings = mappings.strip().split('\n')
    mappings = [m.strip().split(' ') for m in mappings]
    mappings = [Mapping(dest_start=int(t[0]), source_start=int(t[1]), length=int(t[2])) for t in mappings]
    return Map(name, mappings)


def parse_input(f) -> (List[Seed], List[Map]):
    seeds = []
    maps = []
    step = ''
    for line in f:
        line = line.strip()
        if line.startswith('seeds:'):
            seeds = [Seed(value=int(seed), steps=[]) for seed in line.split(': ')[1].split(' ')]
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
    with open('input5.txt') as f:
        seeds, mappings = parse_input(f)
        score = get_lowest_location(seeds, mappings)
        print(score)


if __name__ == "__main__":
    main()
