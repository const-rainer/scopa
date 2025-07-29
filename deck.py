import copy
import random
from card import Card

class Deck:
    def __init__(self):
        self.__cards = [
            Card(value, suit)
            for value in range(1, 11)
            for suit in ['B', 'C', 'D', 'S']
        ]

        self.current_deck = copy.deepcopy(self.__cards)

    def __str__(self):
        return f"current_deck: {self.current_deck}"

    def shuffle(self):
        print("* shuffling deck *")
        random.shuffle(self.current_deck)

    def is_empty(self):
        return len(self.current_deck) == 0

    def get_cards(self, n):
        cards = []
        for i in range(0, n):
            cards.append(self.current_deck.pop(0))

        return cards
