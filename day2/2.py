def main():
    """
    As you continue your walk, the Elf poses a second question: in each game you played,
    what is the fewest number of cubes of each color that could have been in the bag to
    make the game possible?

    The power of a set of cubes is equal to the numbers of red, green, and blue cubes
    multiplied together. The power of the minimum set of cubes in game 1 is 48. In games
    2-5 it was 12, 1560, 630, and 36, respectively. Adding up these five powers
    produces the sum 2286.

    For each game, find the minimum set of cubes that must have been present. What is the 
    sum of the power of these sets?
    """
    with open('input2.txt', 'r') as f:
        total = 0
        for line in f:
            line = line.strip()
            games = line.split(':')[1:][0].split(';')
            game_cubes = {
                'red': 0,
                'green': 0,
                'blue': 0
            }

            for game in games:
                game = game.strip()
                scores = game.split(',')
                for score in scores:
                    score = score.strip()
                    [number, color] = score.split(' ')
                    if game_cubes[color] < int(number):
                        game_cubes[color] = int(number)
            power = 1
            for color, value in game_cubes.items():
                 power *= value

            total += power

    print(total)
    return total


if __name__ == "__main__":
    main()
