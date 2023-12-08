from dataclasses import dataclass
from enum import Enum
from typing import List


@dataclass
class Card:
    value: str
    label: str

    def __repr__(self):
        return self.label

card_labels = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
deck = [Card(hex(value).strip('0x'), label) for value, label in zip(range(2, 15), card_labels)]


class HandType (Enum):
    HIGH_CARD = 0
    ONE_PAIR = 1
    TWO_PAIR = 2
    THREE_OF_A_KIND = 3
    FULL_HOUSE = 4
    FOUR_OF_A_KIND = 5
    FIVE_OF_A_KIND = 6


class Hand:
    cards: List[Card] = []
    bid: int
    type: HandType = HandType.HIGH_CARD

    def __init__(self, cards: List[Card], bid: int):
        self.cards = cards
        self.bid = bid
        self.calculate_type()

    def __repr__(self):
        return f"Hand: value = {self.hand_value()}, type={self.type}, cards = {self.cards} | "

    def calculate_type(self):
        counts = {}
        for card in self.cards:
            if card.label not in counts:
                counts[card.label] = 0
            counts[card.label] += 1
        for card, value in sorted(counts.items(), key=lambda value: value[1]):
            if value == 5:
                self.type = HandType.FIVE_OF_A_KIND
            elif value == 4:
                self.type = HandType.FOUR_OF_A_KIND
            elif value == 3:
                if self.type == HandType.ONE_PAIR:
                    self.type = HandType.FULL_HOUSE
                else:
                    self.type = HandType.THREE_OF_A_KIND
            elif value == 2:
                if self.type == HandType.THREE_OF_A_KIND:
                    self.type = HandType.FULL_HOUSE
                elif self.type == HandType.ONE_PAIR:
                    self.type = HandType.TWO_PAIR
                else:
                    self.type = HandType.ONE_PAIR
            else:
                self.type = HandType.HIGH_CARD

    def hand_value(self):
        return int(str(self.type.value) + ''.join([card.value for card in self.cards]), 16)


def calculate_winnings(hands: List[Hand]) -> int:
    hands.sort(key=lambda hand: hand.hand_value())
    total = 0
    for i, hand in enumerate(hands):
        total += hand.bid * (i + 1)
    return total


def parse_input(f) -> List[Hand]:
    hands = []
    for line in f:
        line = line.strip()
        [hand_str, bid] = line.split(' ')
        hand_cards = [deck[card_labels.index(c)] for c in hand_str]
        hand = Hand(hand_cards, int(bid))
        hands.append(hand)
    return hands


def main():
    with open('../day8/input8.txt') as f:
        hands = parse_input(f)
        winnings = calculate_winnings(hands)
        print(winnings)


if __name__ == "__main__":
    main()
