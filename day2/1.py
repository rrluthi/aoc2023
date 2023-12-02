def main():
    """
    The Elf would first like to know which games would have been possible if the bag
    contained only 12 red cubes, 13 green cubes, and 14 blue cubes?

    In the example above, games 1, 2, and 5 would have been possible if the bag had
    been loaded with that configuration. However, game 3 would have been impossible
    because at one point the Elf showed you 20 red cubes at once; similarly, game 4 
    would also have been impossible because the Elf showed you 15 blue cubes at once.
    If you add up the IDs of the games that would have been possible, you get 8.
    """
    with open('input2.txt', 'r') as f:
        total = 0
        counter = 1
        cube_limits = {
            'red': 12,
            'green': 13,
            'blue': 14
        }
        for line in f:
            line = line.strip()
            games = line.split(':')[1:][0].split(';')
            count_line = True
            for game in games:
                game = game.strip()
                scores = game.split(',')
                for score in scores:
                    score = score.strip()
                    [number, color] = score.split(' ')
                    if cube_limits[color] < int(number):
                        count_line = False
                        break

            if count_line:
                total += counter
            counter += 1

    print(total)
    return total


if __name__ == "__main__":
    main()
