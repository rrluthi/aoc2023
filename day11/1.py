from itertools import combinations


def get_galaxies(universe):
    return [
        (x, y)
        for y, line in enumerate(universe)
        for x, char in enumerate(line)
        if char == "#"
    ]


def expand_universe(universe):
    ys = [i for i, line in enumerate(universe) if "#" not in line]
    xs = [i for i, line in enumerate(zip(*universe)) if "#" not in line]
    len_x = len(universe[-1])
    for y in reversed(ys):
        universe.insert(y, "." * len_x)

    for x in reversed(xs):
        copied = universe.copy()
        for i, line in enumerate(copied):
            universe[i] = line[:x] + "." + line[x:]

    return universe


def parse_input(f):
    universe = []
    for line in f:
        line = line.strip()
        universe.append(line)
    return universe 


def calc_distance(pair):
    (x1, y1), (x2, y2) = pair
    return abs(x1 - x2) + abs(y1 - y2)


def main():
    with open("input11.txt") as f:
        universe = parse_input(f)
        expanded_universe = expand_universe(universe)
        galaxy_coords = get_galaxies(expanded_universe)
        pairs = list(combinations(galaxy_coords, 2))
        result = sum(calc_distance(pair) for pair in pairs)
        print(f"{result=}")


if __name__ == "__main__":
   main() 