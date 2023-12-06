from dataclasses import dataclass
import sys
from typing import List


@dataclass
class Race:
    time: int
    distance: int
    count: int


def get_num_victories(race: Race) -> int:
    for t in range(1, race.time):
        dist_covered = (race.time - t) * t
        if dist_covered > race.distance:
            race.count += 1
    return race.count


def sum_victories(races) -> int:
    count = 1
    for race in races:
        count *= get_num_victories(race)
    return count


def parse_input(f) -> List[Race]:
    times = []
    distances = []
    races = []
    for line in f:
        if line.startswith('Time:'):
            line = line.split(':')[1].strip()
            times = [int(d) for d in list(filter(lambda x: x.isdigit(), line.split(' ')))]
        elif line.startswith('Distance:'):
            line = line.split(':')[1].strip()
            distances = [int(d) for d in list(filter(lambda x: x.isdigit(), line.split(' ')))]

    for time, distance in zip(times, distances):
        races.append(Race(time, distance, 0))
    return races


def main():
    with open('sample6.txt') as f:
        races = parse_input(f)
        victories = sum_victories(races)
        print(victories)


if __name__ == "__main__":
    main()
