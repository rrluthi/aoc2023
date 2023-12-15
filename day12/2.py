import re
from functools import cache
from itertools import chain, repeat


def count_combinations(sequence: str, sizes: tuple[int]) -> int:
    characters = len(sequence)
    number = sizes[0]

    counter = 0
    if len(sizes) > 1:
        for index in range(characters):
            test_str = "." * index + "#" * number + "."

            remaining = sequence[len(test_str):]
            sizes_left = sizes[1:]

            if len(remaining) < sum(sizes_left) + len(sizes_left) - 1:
                break

            if not is_sequence_valid(test_str, sequence[:len(test_str)]):
                continue

            counter += count_combinations(remaining, sizes[1:])
    else:
        for index in range(characters - number + 1):
            test_str = "." * index + "#" * number + "." * (characters - number - index)
            if not is_sequence_valid(test_str, sequence):
                continue

            counter += 1

    return counter


@cache
def is_sequence_valid(sequence: str, validator: str) -> bool:
    if "#" in validator or "." in validator:
        pattern = validator.replace(".", r"\.")
        pattern = pattern.replace("?", ".")
        match = re.match(pattern, sequence)

        if not match:
            return False

    return True


def main():
    with open('input12.txt') as f:
        condition_records = f.read().splitlines()

        total_combinations = 0
        for record in condition_records:
            sequence, nums = record.split(" ")
            nums = tuple(int(num) for num in nums.split(","))
            sequence = "?".join(repeat(sequence, 5))
            nums = tuple(chain.from_iterable(repeat(nums, 5)))

            total_combinations += count_combinations(sequence, nums)

    print(total_combinations)


if __name__ == "__main__":
    main()
