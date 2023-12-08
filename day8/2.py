from dataclasses import dataclass
from itertools import starmap
from enum import Enum
from typing import List


@dataclass
class Card:
    value: str
    label: str

    def __repr__(self):
        return self.label


def create_card(value, label):
    return Card(value, label)


# using base 13 to make the hand value comparison easier
card_labels = ['J', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'Q', 'K', 'A']
card_values = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd']
deck = list(starmap(create_card, zip(card_values, card_labels)))


class HandType (Enum):
    HIGH_CARD = 0
    ONE_PAIR = 1
    TWO_PAIR = 2
    THREE_OF_A_KIND = 3
    FULL_HOUSE = 4
    FOUR_OF_A_KIND = 5
    FIVE_OF_A_KIND = 6
    INVALID_HAND = -1


@dataclass
class Hand:
    cards: List[Card]
    bid: int
    type: HandType


def calc_value(hand) -> str:
    return str(hand.type.value) + ''.join([card.value for card in hand.cards])


def calculate_type(cards):
    counts = {'J': 0}
    j_count = 0
    for card in cards:
        if card.label not in counts:
            counts[card.label] = 0
        counts[card.label] += 1

    if 0 < counts['J'] < 5:
        j_count = counts.pop('J')

    sorted_by_count = sorted(counts.items(), key=lambda x: x[1])
    if j_count:
        highest_count = sorted_by_count.pop()
        sorted_by_count.append((highest_count[0], highest_count[1] + j_count))

    card_type = HandType.INVALID_HAND
    for card, value in sorted_by_count:
        if value < 2:
            card_type = HandType.HIGH_CARD
        elif value == 2:
            if card_type == HandType.THREE_OF_A_KIND:
                card_type = HandType.FULL_HOUSE
            elif card_type == HandType.ONE_PAIR:
                card_type = HandType.TWO_PAIR
            else:
                card_type = HandType.ONE_PAIR
        elif value == 3:
            if card_type == HandType.ONE_PAIR:
                card_type = HandType.FULL_HOUSE
            else:
                card_type = HandType.THREE_OF_A_KIND
        elif value == 4:
            card_type = HandType.FOUR_OF_A_KIND
        elif value == 5:
            card_type = HandType.FIVE_OF_A_KIND

    return card_type


def calculate_winnings(hands: List[Hand]) -> int:
    hands.sort(key=lambda h: calc_value(h))
    total = 0
    for i, hand in enumerate(hands):
        total += hand.bid * (i + 1)
    return total


def parse_input(f) -> List[Hand]:
    hands = []
    for line in f:
        line = line.strip()
        # split the line into the hand and the bid
        [hand_str, bid] = line.split(' ')
        # convert the hand string into a list of cards
        hand_cards = [deck[card_labels.index(c)] for c in hand_str]
        # create a hand object
        hand = Hand(cards=hand_cards, bid=int(bid), type=calculate_type(hand_cards))
        hands.append(hand)
    return hands


def main():
    with open('input7.txt') as f:
        hands = parse_input(f)
        winnings = calculate_winnings(hands)
        print(winnings)


if __name__ == "__main__":
    main()