from functools import reduce

char_matrix = []


def is_symbol(char) -> bool:
    return not char.isdigit() and char != '.'


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
                line_array.append(char)
            char_matrix.append(line_array)


def symbol_adjacent(row, col) -> bool:
    """
    check if a symbol is adjacent to a point, above, below, left, right and diagonal
    :return: Boolean
    """
    adjacent = False
    if row > 0:  # above
        if is_symbol(char_matrix[row - 1][col]):
            adjacent = True
    if row < len(char_matrix) - 1:  # below
        if is_symbol(char_matrix[row + 1][col]):
            adjacent = True
    if col > 0:  # left
        if is_symbol(char_matrix[row][col - 1]):
            adjacent = True
    if col < len(char_matrix[row]) - 1:  # right
        if is_symbol(char_matrix[row][col + 1]):
            adjacent = True
    if row > 0 and col > 0:  # diagonal
        if is_symbol(char_matrix[row - 1][col - 1]):
            adjacent = True
    if row > 0 and col < len(char_matrix[row]) - 1:  # diagonal
        if is_symbol(char_matrix[row - 1][col + 1]):
            adjacent = True
    if row < len(char_matrix) - 1 and col > 0:  # diagonal
        if is_symbol(char_matrix[row + 1][col - 1]):
            adjacent = True
    if row < len(char_matrix) - 1 and col < len(char_matrix[row]) - 1:  # diagonal
        if is_symbol(char_matrix[row + 1][col + 1]):
            adjacent = True

    return adjacent


def get_entire_number(row, col, number_list) -> []:
    """
    check if a number is part of a larger number, checking left and right sides.
    return the assembled number as a string
    :param col: int
    :param row: int
    :param number_list: []
    :return: []
    """
    for i in range(col + 1, len(char_matrix[row])):
        if char_matrix[row][i].isdigit():
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
            if char_matrix[row][col].isdigit():
                number.append([row, col])
            if len(number) > 0:
                number = get_entire_number(row, col, number)
                near_symbol = False
                for point_row, point_col in number:
                    if symbol_adjacent(point_row, point_col):
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
