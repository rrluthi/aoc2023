from dataclasses import dataclass
from enum import Enum
from typing import List


@dataclass
class Card:
    value: str
    label: str

    def __repr__(self):
        return self.label


card_labels = ['J', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'Q', 'K', 'A']
deck = [Card(hex(value).strip('0x'), label) for value, label in zip(range(1, 14), card_labels)]


class HandType (Enum):
    HIGH_CARD = 0
    ONE_PAIR = 1
    TWO_PAIR = 2
    THREE_OF_A_KIND = 3
    FULL_HOUSE = 4
    FOUR_OF_A_KIND = 5
    FIVE_OF_A_KIND = 6
    INVALID_HAND = -1


class Hand:
    cards: List[Card] = []
    bid: int
    type: HandType = HandType.HIGH_CARD

    def __init__(self, cards: List[Card], bid: int):
        self.cards = cards
        self.bid = bid
        self.calculate_type()

    def __repr__(self):
        return f"Hand: value = {self.hand_value()}, type={self.type.name}, bid={self.bid}"

    def calculate_type(self):
        counts = {'J': 0}
        j_count = 0
        for card in self.cards:
            if card.label not in counts:
                counts[card.label] = 0
            counts[card.label] += 1

        if 0 < counts['J'] < 5:
            j_count = counts.pop('J')

        sorted_by_count = sorted(counts.items(), key=lambda x: x[1])
        if j_count:
            highest_count = sorted_by_count.pop()
            sorted_by_count.append((highest_count[0], highest_count[1] + j_count))

        for card, value in sorted_by_count:
            if value < 2:
                self.type = HandType.HIGH_CARD
            elif value == 2:
                if self.type == HandType.THREE_OF_A_KIND:
                    self.type = HandType.FULL_HOUSE
                elif self.type == HandType.ONE_PAIR:
                    self.type = HandType.TWO_PAIR
                else:
                    self.type = HandType.ONE_PAIR
            elif value == 3:
                if self.type == HandType.ONE_PAIR:
                    self.type = HandType.FULL_HOUSE
                else:
                    self.type = HandType.THREE_OF_A_KIND
            elif value == 4:
                self.type = HandType.FOUR_OF_A_KIND
            elif value == 5:
                self.type = HandType.FIVE_OF_A_KIND
            else:
                self.type = HandType.INVALID_HAND

    def hand_value(self):
        return str(self.type.value) + ''.join([card.value for card in self.cards])


def calculate_winnings(hands: List[Hand]) -> int:
    hands.sort(key=lambda hand: hand.hand_value())
    total = 0
    for i, hand in enumerate(hands):
        # print(i+1, hand)
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
    with open('input7.txt') as f:
        hands = parse_input(f)
        winnings = calculate_winnings(hands)
        print(winnings)


if __name__ == "__main__":
    main()
