import copy
import random
from itertools import combinations
from enum import Enum
from typing import List

class Suit(Enum):
    B = 1
    C = 2
    D = 3
    S = 4    


class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

    def __repr__(self):
        return f"({self.value}, {self.suit})"

class Deck:
    def __init__(self):
        self.cards = [
            Card(value, suit)
            for value in range(1, 11)
            for suit in [s.name for s in Suit]
        ]

        self.current_deck = copy.deepcopy(self.cards)

    def __str__(self):
        return f"current_deck: {self.current_deck}"

    def shuffle(self):
        print("* shuffling deck *")
        random.shuffle(self.current_deck)

    def get_cards(self, n):
        cards = []
        for i in range(0, n):
            cards.append(self.current_deck.pop(0))

        return cards

    def reset(self):
        self.current_deck = copy.deepcopy(self.deck)


class CardGame:
    def __init__(self):
        self.deck = Deck()
        self.players = [Player(1), Player(2)]
        self.upcards = []

    def init_game(self):
        self.deck.shuffle()

        for upcard in self.deck.get_cards(4):
            self.upcards.append(upcard)

        self.players[0].currently_playing = True

    def game(self):
        self.init_game()
        n_mano = 1

        while self.game_ongoing():
            if all(not player.has_cards() for player in self.players):
                print(f"\n\n------- MANO {n_mano} -------")
                n_mano = n_mano + 1
                for player in self.players:
                    hand = self.deck.get_cards(3)
                    player.set_cards(hand)

            player = self.update_active_player()
            print(player)
            print(f"Carte sul tavolo: {self.upcards}")

            played_card, picked_cards = player.play_card(self.upcards)
            self.update_upcards(played_card, picked_cards)
            print("\n")

    def get_active_player(self):
        for i in range(len(self.players)):
            if self.players[i].currently_playing:
                return self.players[i]

    def update_active_player(self):
        for i in range(len(self.players)):
            if self.players[i].currently_playing:
                self.players[i].currently_playing = False
                i = (i + 1) % len(self.players)
                self.players[i].currently_playing = True
                return self.players[i]

    def update_upcards(self, played_card: Card, picked_cards: List[Card]):
        print(f"Player played card: {played_card}")

        # butto una carta senza prendere niente
        if picked_cards is None: 
            self.upcards.append(played_card)
        
        # ho almeno una carta da prendere
        else:
            for card in picked_cards:
                self.upcards.remove(card)            

    def game_ongoing(self):
        deck_has_cards = (len(self.deck.current_deck) > 0)
        players_have_cards = any([player.has_cards() for player in self.players])

        return deck_has_cards or players_have_cards


class Player:
    def __init__(self, n):
        self.n = n
        self.currently_playing = False
        self.cards = []
        self.score = 0

    def __repr__(self):
        return f"Player: [n = {self.n}, currently_playing = {self.currently_playing}, cards = {self.cards}, score = {self.score}]"

    def play_card(self, upcards):
        played_card = None
        picked_cards = None

        if len(upcards) == 0:    
            # play an arbitrary card and pick nothing
            played_card = self.__get_random_card()
        
        elif len(upcards) == 1:
            # there is at most one card to pick
            # try to make scopa
            played_card, picked_cards = self.__match_single_upcard(upcards)

        else:
            # get all possible picks
            played_card, picked_cards = self.__choose_best_pick(upcards)
        
        self.cards.remove(played_card)
        return played_card, picked_cards

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

    def has_cards(self):
        return len(self.cards) > 0

    def set_cards(self, cards):
        self.cards = cards

if __name__ == '__main__':
    card_game = CardGame()
    card_game.game()
