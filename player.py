from card import Card
from deck import Deck
from itertools import combinations
from score import Score
import random

class Player:
    def __init__(self, n):
        self.n = n
        self.cards = []
        self.score = Score()

    def __repr__(self):
        return f"Player: [n = {self.n}, cards = {self.cards}, score = {self.score}]"

    def has_cards(self):
        return len(self.cards) > 0

    def set_cards(self, cards):
        self.cards = cards

    def get_score(self):
        return self.score

    def get_cards(self):
        return self.cards

    def play_card(self, upcards):
        played_card = None
        picked_cards = None
        scopa = False

        if len(upcards) == 0:    
            # play an arbitrary card and pick nothing
            played_card = self.__get_random_card()
        
        elif len(upcards) == 1:
            # there is at most one card to pick
            # try to make scopa
            played_card, picked_cards = self.__match_single_upcard(upcards)
            if picked_cards == upcards:
                scopa = True

        else:
            # get all possible picks
            played_card, picked_cards = self.__choose_best_pick(upcards)

        print(f"Player played card: {played_card}")
        if picked_cards != None:
            print(f"Player picked cards: {picked_cards}")

        if scopa:
            print("SCOPA!!")

        self.score.add_cards(played_card, picked_cards, scopa)
        self.cards.remove(played_card)
        
        return played_card, picked_cards

    def add_to_score(self, cards):
        self.score.add_last_cards(cards)

    def __choose_best_pick(self, upcards):
        played_card = None
        picked_cards = None

        possible_picks = self.__get_all_possible_picks(upcards)
        print(f"possible_picks: {possible_picks}")

        if len(possible_picks.items()) > 0:
            # choose one pick
            played_card, picked_cards = random.choice(list(possible_picks.items()))
        else:
            # nothing to pick. play one random card.
            played_card = self.__get_random_card()

        return played_card, picked_cards

    
    def __get_all_possible_picks(self, upcards):
        possible_picks = {}
        for i in range(len(upcards)+1):
            upcards_combinations = combinations(upcards, i)
            for combination in upcards_combinations:
                #print(f"combinations: {combination}")
                total_pick_value = 0
                for card in combination:
                    total_pick_value = total_pick_value + card.value
                for card in self.cards:
                    if card.value == total_pick_value:
                        possible_picks[card] = combination
        
        return possible_picks

    def __get_random_card(self):
        return self.cards[0]
    
    def __match_single_upcard(self, upcards):
        scopa = next((x for x in self.cards if x.value == upcards[0].value), None)
        if scopa != None:
            # we made scopa
            return scopa, upcards
        
        # couldn't make scopa. play a card that doesn't sum with 7 (if possible)
        match = next((x for x in self.cards if x.value + upcards[0].value != 7), None)
        if match != None:
            return match, None
        
        return self.__get_random_card(), None