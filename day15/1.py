

def hash_step(value, step):
    if len(step) == 0:
        return value
    char_code = ord(step[0])
    value += char_code
    value *= 17
    value %= 256
    # print(value)
    return hash_step(value, step[1:])


def parse_input(f):
    steps = []
    for line in f:
        line = line.strip()
        steps = line.split(',')
    return steps


def main():
    with open('input15.txt') as f:
        steps = parse_input(f)
        print(sum([hash_step(0, step) for step in steps]))


if __name__ == "__main__":
    main()