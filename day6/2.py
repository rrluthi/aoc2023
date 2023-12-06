from dataclasses import dataclass
from functools import reduce


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


def parse_input(f) -> Race:
    time = 0
    distance = 0
    for line in f:
        if line.startswith('Time:'):
            line = line.split(':')[1].strip()
            time = int(reduce(lambda x, y: x + y, list(filter(lambda x: x.isdigit(), line.split(' '))), ''))
        elif line.startswith('Distance:'):
            line = line.split(':')[1].strip()
            distance = int(reduce(lambda x, y: x + y, list(filter(lambda x: x.isdigit(), line.split(' '))), ''))

    race = Race(time, distance, 0)
    print(race)
    return race


def main():
    with open('input6.txt') as f:
        race = parse_input(f)
        victories = get_num_victories(race)
        print(victories)


if __name__ == "__main__":
    main()
