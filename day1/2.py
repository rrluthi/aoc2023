
INTS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
INT_STRINGS = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
INT_STRINGS_REVERSED = ['eno', 'owt', 'eerht', 'ruof', 'evif', 'xis', 'neves', 'thgie', 'enin']


def find_first_digit(line):
    str_index_found = float('inf')
    stored_i = float('inf')
    for i, num in enumerate(INT_STRINGS):
        index = line.find(num)
        if index != -1 and index < str_index_found:
            stored_i = i
            str_index_found = index
    first_digit = str(stored_i + 1)

    for i, char in enumerate(line):
        if i > str_index_found:
            break
        if char in INTS:
            first_digit = char
            break

    return first_digit


def find_last_digit(line):
    str_index_found = float('inf')
    stored_i = float('inf')
    reversed_line = line[::-1]
    for i, num in enumerate(INT_STRINGS_REVERSED):
        index = reversed_line.find(num)
        if index != -1 and index < str_index_found:
            str_index_found = index
            stored_i = i

    last_digit = str(stored_i + 1)

    for i, char in enumerate(reversed_line):
        if i > str_index_found:
            break
        if char in INTS:
            last_digit = char
            break

    return last_digit


def main():
    """
    open file and read line by line
    :return: 
    """
    with open('input1.txt', 'r') as f:
        total = 0
        for line in f:
            line_num = find_first_digit(line) + find_last_digit(line)
            total += int(line_num)

    print(total)
    return total


if __name__ == "__main__":
    main()