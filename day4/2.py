import functools


LINES = {}


@functools.cache
def process_game(card, game):
    deck, hand = game.strip().split("|")
    deck = list(filter(lambda x: x.isdigit(), deck.split(" ")))
    hand = list(filter(lambda x: x.isdigit(), hand.split(" ")))

    found_cards = []
    for deck_card in deck:
        if deck_card in hand:
            found_cards.append(deck_card)

    line_score = 1
    for i in range(1, len(found_cards) + 1):
        line_score += process_game(int(card) + i, LINES[str(int(card) + i)])

    return line_score


def score_game(lines):
    score = 0
    for card, game in lines.items():
        line_score = process_game(card, game)
        score += line_score
    return score


def main():
    with open('sample4.txt') as f:
        for line in f:
            line = line.strip()
            line = line.strip()
            card, game = line.split(":")
            card = list(filter(lambda x: x.isdigit(), card.split(" ")))[0]
            LINES.update({card: game})

        score = score_game(LINES)
        print(score)


if __name__ == "__main__":
    main()
