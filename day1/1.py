

def main():
    """
    open file and read line by line
    :return: 
    """
    with open('input1.txt', 'r') as f:
        total = 0
        ints = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        for line in f:
            line_num = ''
            for char in line:
                if char in ints:
                    line_num += char
                    break
            for char in reversed(line):
                if char in ints:
                    line_num += char
                    break
            total += int(line_num)
                
    print(total)
    return total


if __name__ == "__main__":
    main()