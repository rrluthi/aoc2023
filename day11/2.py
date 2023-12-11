from itertools import combinations


def get_galaxies(universe):
    galaxies = []
    for y, line in enumerate(universe):
        for x, char in enumerate(line):
            if char == "#":
                galaxies.append((x, y))
    return galaxies


def expand_x(universe):
    return [i for i, line in enumerate(zip(*universe)) if "#" not in line]


def expand_y(universe):
    return [i for i, line in enumerate(universe) if "#" not in line]


def calc_distance(pair, x_exp, y_exp, expansion_factor):
    (x1, y1), (x2, y2) = pair
    most_left = min(x1, x2)
    most_right = max(x1, x2)
    most_high = min(y1, y2)
    most_low = max(y1, y2)

    dx, dy = 0, 0
    for x in x_exp:
        if x in range(most_left, most_right):
            dx += 1
    for y in y_exp:
        if y in range(most_high, most_low):
            dy += 1

    extra_distance = expansion_factor * dx + expansion_factor * dy
    return most_right - most_left + most_low - most_high + extra_distance


def parse_input(f):
    universe = []
    for line in f:
        line = line.strip()
        universe.append(line)
    return universe


def main():
    with open("input11.txt") as f:
        universe = parse_input(f)
        expanded_x = expand_x(universe)
        expanded_y = expand_y(universe)

        galaxy_coords = get_galaxies(universe)
        pairs = list(combinations(galaxy_coords, 2))
        print(f"{len(pairs)=}")
        expand = 1000_000 - 1
        distances = sum(calc_distance(pair, expanded_x, expanded_y, expand) for pair in pairs)
        print(distances)


if __name__ == "__main__":
    main()
