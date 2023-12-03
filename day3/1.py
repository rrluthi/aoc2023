from functools import reduce
from typing import Tuple, Any

numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
non_symbol_list = ['.'] + numbers
symbol_list = []
char_matrix = []


def build_matrix(file) -> None:
    """
    build a matrix of the map
    :return:
    """
    with open(file, 'r') as f:
        for line in f:
            line_array = []
            for char in line:
                if char == '\n':
                    continue
                if char not in non_symbol_list and char not in symbol_list:
                    symbol_list.append(char)
                line_array.append(char)
            char_matrix.append(line_array)


def symbol_adjacent(row, col, symbols: []) -> bool:
    """
    check if a symbol is adjacent to a point, above, below, left, right and diagonal
    :return: Boolean
    """
    adjacent = False
    if row > 0:  # above
        if char_matrix[row - 1][col] in symbols:
            adjacent = True
    if row < len(char_matrix) - 1:  # below
        if char_matrix[row + 1][col] in symbols:
            adjacent = True
    if col > 0:  # left
        if char_matrix[row][col - 1] in symbols:
            adjacent = True
    if col < len(char_matrix[row]) - 1:  # right
        if char_matrix[row][col + 1] in symbols:
            adjacent = True
    if row > 0 and col > 0:  # diagonal
        if char_matrix[row - 1][col - 1] in symbols:
            adjacent = True
    if row > 0 and col < len(char_matrix[row]) - 1:  # diagonal
        if char_matrix[row - 1][col + 1] in symbols:
            adjacent = True
    if row < len(char_matrix) - 1 and col > 0:  # diagonal
        if char_matrix[row + 1][col - 1] in symbols:
            adjacent = True
    if row < len(char_matrix) - 1 and col < len(char_matrix[row]) - 1:  # diagonal
        if char_matrix[row + 1][col + 1] in symbols:
            adjacent = True

    return adjacent


def is_part_of_larger_number(row, col, number_list) -> []:
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
                number = is_part_of_larger_number(row, col, number)
                near_symbol = False
                for point in number:
                    [point_row, point_col] = point
                    if symbol_adjacent(point_row, point_col, symbol_list):
                        near_symbol = True
                if near_symbol:
                    num = int(reduce(lambda x, y: x + y, [char_matrix[row][col] for row, col in number], ''))
                    total += num
                col += len(number)
            else:
                col += 1
    print(total)


if __name__ == "__main__":
    main()
