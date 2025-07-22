import copy
import random

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

    def print_current_deck(self):
        print(f"current_deck: {self.current_deck}")


class CardGame:
    def __init__(self):
        self.deck = Deck()
        self.players = [Player(), Player()]
        self.upcards = []

    def init_game(self):
        deck.shuffle()
        
        for player in self.players:
            player.set_cards(deck.get_cards(3))
        
        for upcard in deck.get_cards(4):
            upcards.append(card)

        players[0].currently_playing = True

    def game(self):
        init_game()

        while game_ongoing():
            player = get_active_player()
            card = player.get_best_card(upcards)
            play_card(card)

    def get_active_player(self):
        for i in range(len(players)):
            if players[i].currently_playing:
                players[i].currently_playing = False
                i = (i+1)%len(players)
                players[i].currently_playing = True
                return players[i]

    def play_card(self):
        pass

    def game_ongoing(self):
        game_ongoing = False
        for player in players:
            game_ongoing = game_ongoing or player.has_cards()

        return game_ongonig
        

class Player:
    def __init__(self):
        self.currently_playing = False
        self.cards = []
        self.score = 0

    def get_best_card(self, upcards):
        card = None

        if len(upcards) == 0:
            card = self.cards.pop(0)
            return card

        for upcard in upcards:
            for i in range(len(cards)):
                

    def has_cards(self):
        return len(self.cards) > 0


if __name__ == '__main__':





''' 
players = [player1, player2]

game.play_hand(self, ):
    hand = deck.get_hand()
    while len(players) is not 0:
        player = 
        card = player1.select_card(hand)
        player1.play_card(card)





'''