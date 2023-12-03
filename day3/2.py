from functools import reduce
from typing import Tuple, Any

numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
non_symbol_list = ['.'] + numbers
symbol_list = ['*']
char_matrix = []
gear_map = {}


def build_matrix(file) -> None:
    """
    build a matrix of the map
    :return:
    """
    with open(file, 'r') as f:
        for i, line in enumerate(f):
            line_array = []
            for j, char in enumerate(line):
                if char == '\n':
                    continue
                if char not in non_symbol_list and char not in symbol_list:
                    symbol_list.append(char)
                line_array.append(char)
                gear_map[(i, j)] = []
            char_matrix.append(line_array)


def get_gears(row: int, col: int, number: [], symbols: []) -> bool:
    """
    check if a symbol is adjacent to a point, above, below, left, right and diagonal
    :return: Boolean
    """
    adjacent = False
    if row > 0:  # above
        if char_matrix[row - 1][col] in symbols and number not in gear_map[(row - 1, col)]:
            gear_map[(row - 1, col)].append(number)
    if row < len(char_matrix) - 1:  # below
        if char_matrix[row + 1][col] in symbols and number not in gear_map[(row + 1, col)]:
            gear_map[(row + 1, col)].append(number)
    if col > 0:  # left
        if char_matrix[row][col - 1] in symbols and number not in gear_map[(row, col - 1)]:
            gear_map[(row, col - 1)].append(number)
    if col < len(char_matrix[row]) - 1:  # right
        if char_matrix[row][col + 1] in symbols and number not in gear_map[(row, col + 1)]:
            gear_map[(row, col + 1)].append(number)
    if row > 0 and col > 0:  # diagonal upper left
        if char_matrix[row - 1][col - 1] in symbols and number not in gear_map[(row - 1, col - 1)]:
            gear_map[(row - 1, col - 1)].append(number)
    if row > 0 and col < len(char_matrix[row]) - 1:  # diagonal upper right
        if char_matrix[row - 1][col + 1] in symbols and number not in gear_map[(row - 1, col + 1)]:
            gear_map[(row - 1, col + 1)].append(number)
    if row < len(char_matrix) - 1 and col > 0:  # diagonal lower left
        if char_matrix[row + 1][col - 1] in symbols and number not in gear_map[(row + 1, col - 1)]:
            gear_map[(row + 1, col - 1)].append(number)
    if row < len(char_matrix) - 1 and col < len(char_matrix[row]) - 1:  # diagonal lower right
        if char_matrix[row + 1][col + 1] in symbols and number not in gear_map[(row + 1, col + 1)]:
            gear_map[(row + 1, col + 1)].append(number)

    return adjacent


def get_entire_number(row, col, number_list) -> []:
    """
    check if a number is part of a larger number, checking left and right sides.
    return the assembled number as a string
    :param number: []
    :return: []
    """
    for i in range(col + 1, len(char_matrix[row])):
        if char_matrix[row][i] in numbers:
            number_list.append([row, i])
        else:
            break

    return number_list


def main():
    """
    open file and read line by line
    Fill out a map with rows and columns and at each point designate what is at that location
    :return: 
    """
    build_matrix('input3.txt')
    total = 0
    for row in range(len(char_matrix)):
        col = 0
        while col < len(char_matrix[row]):
            number = []
            if char_matrix[row][col] in numbers:
                number.append([row, col])
            if len(number) > 0:
                entire_number = get_entire_number(row, col, number)
                for point in entire_number:
                    [point_row, point_col] = point
                    get_gears(point_row, point_col, number, symbol_list)
                col += len(entire_number)
            else:
                col += 1

    for key, value in gear_map.items():
        if len(value) == 2:
            product = 1
            for number in value:
                product *= int(reduce(lambda x, y: x + y, [char_matrix[row][col] for row, col in number], ''))
            total += product
    print(total)


if __name__ == "__main__":
    main()
