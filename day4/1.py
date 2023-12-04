
def score_game(f):
    score = 0
    for line in f:
        line = line.strip()
        card, game = line.split(":")
        deck, hand = game.strip().split("|")
        deck = list(filter(lambda x: x.isdigit(), deck.split(" ")))
        hand = list(filter(lambda x: x.isdigit(), hand.split(" ")))
        line_score = 0
        found_cards = []
        for i, card in enumerate(hand):
            if hand[i] in deck:
                found_cards.append(hand[i])
                if len(found_cards) == 1:
                    line_score += 1
                else:
                    line_score *= 2
                deck.remove(hand[i])
        score += line_score
    return score


def main():
    with open('input4.txt') as f:
        score = score_game(f)
        print(score)


if __name__ == "__main__":
    main()