import copy
import random
from itertools import combinations

class Deck:
    def __init__(self):
        ''' I semi delle carte sono identificati dalla lettera:
            'B' : bastoni
            'C' : coppe
            'D' : denari
            'S' : spade

            Il valore delle carte va da 1 (asso) fino a 10 (re)
        '''
        self.deck = [(1, "B"), (2, "B"), (3, "B"), (4, "B"), (5, "B"), (6, "B"), (7, "B"), (8, "B"), (9, "B"), (10, "B"), 
                     (1, "C"), (2, "C"), (3, "C"), (4, "C"), (5, "C"), (6, "C"), (7, "C"), (8, "C"), (9, "C"), (10, "C"), 
                     (1, "D"), (2, "D"), (3, "D"), (4, "D"), (5, "D"), (6, "D"), (7, "D"), (8, "D"), (9, "D"), (10, "D"), 
                     (1, "S"), (2, "S"), (3, "S"), (4, "S"), (5, "S"), (6, "S"), (7, "S"), (8, "S"), (9, "S"), (10, "S") ] 

        self.current_deck = copy.deepcopy(self.deck)

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
        self.players = [Player(), Player()]
        self.upcards = []

    def init_game(self):
        self.deck.shuffle()

        for player in self.players:
            player.set_cards(self.deck.get_cards(3))

        for upcard in self.deck.get_cards(4):
            self.upcards.append(upcard)

        self.players[0].currently_playing = True

    def game(self):
        self.init_game()

        for player in self.players:
            print(f"{player}")
        #print(f"{self.deck}")
        print(f"Carte sul tavolo: {self.upcards}")

        while self.game_ongoing():
            player = self.get_active_player()
            card, opportunity = player.get_best_card(self.upcards)
            self.play_card(card, opportunity)
            print(f"Carte sul tavolo: {self.upcards}")
            return

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

    def play_card(self, card, opportunity):
        print(f"Player played card: {card}")
        if opportunity is not None:
            for o in opportunity:
                for i in range(len(self.upcards)):
                    if o[0] == self.upcards[i][0]:
                        self.upcards.pop(i)
                        break
        else:
            self.upcards.append(card)

    def game_ongoing(self):
        game_ongoing = False
        for player in self.players:
            game_ongoing = game_ongoing or player.has_cards()

        return game_ongoing


class Player:
    def __init__(self):
        self.currently_playing = False
        self.cards = []
        self.score = 0

    def __str__(self):
        return f"Player: [currently_playing = {self.currently_playing}, cards = {self.cards}, score = {self.score}]"


    def get_best_card(self, upcards):
        if len(upcards) == 0:
            return self.cards.pop(0), upcards
        elif len(upcards) == 1:
            match = next((x for x in self.cards if x[0] == upcards[0][0]), None)
            if match != None:
                return match, upcards

            match = next((x for x in self.cards if x[0] + upcards[0][0] != 7), None)
            if match != None:
                return match, upcards

        opportunities = {}
        for i in range(len(upcards)):
            for card_combination in combinations(upcards, i):
                print(f"combinations: {card_combination}")
                total_value = 0
                for card in card_combination:
                    total_value = total_value + card[0]
                if total_value <= 10:
                    opportunities[total_value] = card_combination
        print(f"opportunities: {opportunities}")

        for i in range(len(self.cards)):
            for opportunity in opportunities.keys():
                if self.cards[i][0] == opportunity:
                    return self.cards.pop(i), opportunities[opportunity]

        return self.cards.pop(0), None


    def has_cards(self):
        return len(self.cards) > 0

    def set_cards(self, cards):
        self.cards = cards

if __name__ == '__main__':
    card_game = CardGame()
    card_game.game()
