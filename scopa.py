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
        self.__cards = [
            Card(value, suit)
            for value in range(1, 11)
            for suit in [s.name for s in Suit]
        ]

        self.current_deck = copy.deepcopy(self.__cards)

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

    def __init_game(self):
        self.deck.shuffle()

        for upcard in self.deck.get_cards(4):
            self.upcards.append(upcard)

        self.players[0].set_playing()

    def game(self):
        self.__init_game()
        n_mano = 1
        last_to_pick = None

        # main loop
        while self.__game_ongoing():
            if all(not player.has_cards() for player in self.players):
                print(f"\n\n------- MANO {n_mano} -------")
                n_mano = n_mano + 1
                for player in self.players:
                    hand = self.deck.get_cards(3)
                    player.set_cards(hand)

            player = self.__update_active_player()
            print(player)
            print(f"Carte sul tavolo: {self.upcards}")

            played_card, picked_cards = player.play_card(self.upcards)
            self.__update_upcards(played_card, picked_cards)

            if picked_cards != None:
                last_to_pick = player

            print("\n")

        # Game is over. If upcards remain, last player to pick gets them all.
        if(len(self.upcards) > 0):
            print(f"Player {last_to_pick.n} picks all!! ({self.upcards})\n")
            last_to_pick.add_to_score(self.upcards)


        print(" ***** FINAL SCORE ***** ")
        for player in self.players:
            print(f"Player {player.n}: {player.get_score()}")

    def __update_active_player(self):
        for i in range(len(self.players)):
            if self.players[i].is_playing():
                self.players[i].stop_playing()
                i = (i + 1) % len(self.players)
                self.players[i].set_playing()
                return self.players[i]

    def __update_upcards(self, played_card: Card, picked_cards: List[Card]):
        # butto una carta senza prendere niente
        if picked_cards is None: 
            self.upcards.append(played_card)
        
        # ho almeno una carta da prendere
        else:
            for card in picked_cards:
                self.upcards.remove(card)            

    def __game_ongoing(self):
        deck_has_cards = (len(self.deck.current_deck) > 0)
        players_have_cards = any([player.has_cards() for player in self.players])

        return deck_has_cards or players_have_cards


class Player:
    def __init__(self, n):
        self.n = n
        self.__cards = []
        self.__score = Score()
        self.__currently_playing = False

    def __repr__(self):
        return f"Player: [n = {self.n}, currently_playing = {self.__currently_playing}, cards = {self.__cards}, score = {self.__score}]"

    def has_cards(self):
        return len(self.__cards) > 0

    def set_cards(self, cards):
        self.__cards = cards

    def is_playing(self):
        return self.__currently_playing
    
    def set_playing(self):
        self.__currently_playing = True

    def stop_playing(self):
        self.__currently_playing = False

    def get_score(self):
        return self.__score

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


        self.__score.add_cards(played_card, picked_cards, scopa)
        self.__cards.remove(played_card)
        
        return played_card, picked_cards

    def add_to_score(self, cards):
        self.__score.add_last_cards(cards)

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
                for card in self.__cards:
                    if card.value == total_pick_value:
                        possible_picks[card] = combination
        
        return possible_picks

    def __get_random_card(self):
        return self.__cards[0]
    
    def __match_single_upcard(self, upcards):
        scopa = next((x for x in self.__cards if x.value == upcards[0].value), None)
        if scopa != None:
            # we made scopa
            return scopa, upcards
        
        # couldn't make scopa. play a card that doesn't sum with 7 (if possible)
        match = next((x for x in self.__cards if x.value + upcards[0].value != 7), None)
        if match != None:
            return match, None
        
        return self.__get_random_card(), None
    
class Score:
    def __init__(self):
        self.__picked_cards : List[Card] = []
        self.__scope : List[Card] = []
        self.__settebello : bool = False
        self.__denari : int = 0
        self.__primiera : int = 0

    def add_cards(self, played_card, picked_cards, scopa):
        #add_cards_str = f"Currently picked cards: {self.__picked_cards}\n"

        if picked_cards is not None:
            #add_cards_str += f"Adding played cards: {played_card}"
            self.__picked_cards.append(played_card)
            #add_cards_str += f", and picked cards: {picked_cards}"
            self.__picked_cards.extend(picked_cards)
            if scopa:
                self.__scope.append(played_card)

        #add_cards_str += f"\nNew self.__picked_cards: {self.__picked_cards}"

        #print(add_cards_str)

        self.__update_score()

    def add_last_cards(self, last_cards):
        self.__picked_cards.extend(last_cards)
        self.__update_score()

    def __update_score(self):
        if not self.__settebello:
            self.__settebello = any(card.value == 7 and card.suit == 'D' 
                                    for card in self.__picked_cards)
        
        self.__primiera = self.__calc_primiera()
        self.__denari = len([card for card in self.__picked_cards if card.suit == 'D'])

    def __repr__(self):
        score_string = ""
        score_string += f"Carte: {len(self.__picked_cards)}, "
        score_string += f"Denari: {self.__denari}, "
        score_string += f"Primiera: {self.__primiera}, "
        score_string += f"Scope: {len(self.__scope)}, "
        score_string += f"Settebello: {self.__settebello}."

        return score_string


    def __calc_primiera(self):
        card_scores = {
             7 : 21,
             6 : 18,
             1 : 16,
             5 : 15,
             4 : 14,
             3 : 13,
             2 : 12,
             8 : 10,
             9 : 10,
            10 : 10
        }

        scores_denari = [card_scores[card.value] for card in self.__picked_cards if card.suit == 'D']
        if len(scores_denari) == 0:
            return 0
        
        scores_bastoni = [card_scores[card.value] for card in self.__picked_cards if card.suit == 'B']
        if len(scores_bastoni) == 0:
            return 0
        
        scores_coppe = [card_scores[card.value] for card in self.__picked_cards if card.suit == 'C']
        if len(scores_coppe) == 0:
            return 0
        
        scores_spade = [card_scores[card.value] for card in self.__picked_cards if card.suit == 'S']
        if len(scores_spade) == 0:
            return 0
        
        scores_denari.sort()
        scores_bastoni.sort()
        scores_coppe.sort()
        scores_spade.sort()

        return (scores_denari[0] + scores_bastoni[0] + 
                scores_spade[0] + scores_coppe[0])

if __name__ == '__main__':
    card_game = CardGame()
    card_game.game()
