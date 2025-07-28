import socket
import time
from itertools import combinations
import random
from typing import List

class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

    def __repr__(self):
        return f"({self.value}, {self.suit})"
    
class Score:
    def __init__(self):
        self.picked_cards : List[Card] = []
        self.scope : List[Card] = []
        self.settebello : bool = False
        self.denari : int = 0
        self.primiera : int = 0

    def add_cards(self, played_card, picked_cards, scopa):
        #add_cards_str = f"Currently picked cards: {self.picked_cards}\n"

        if picked_cards is not None:
            #add_cards_str += f"Adding played cards: {played_card}"
            self.picked_cards.append(played_card)
            #add_cards_str += f", and picked cards: {picked_cards}"
            self.picked_cards.extend(picked_cards)
            if scopa:
                self.scope.append(played_card)

        #add_cards_str += f"\nNew self.picked_cards: {self.picked_cards}"

        #print(add_cards_str)

        self.update_score()

    def add_last_cards(self, last_cards):
        self.picked_cards.extend(last_cards)
        self.update_score()

    def update_score(self):
        if not self.settebello:
            self.settebello = any(card.value == 7 and card.suit == 'D' 
                                    for card in self.picked_cards)
        
        self.primiera = self.calc_primiera()
        self.denari = len([card for card in self.picked_cards if card.suit == 'D'])

    def __repr__(self):
        score_string = ""
        score_string += f"Carte: {len(self.picked_cards)}, "
        score_string += f"Denari: {self.denari}, "
        score_string += f"Primiera: {self.primiera}, "
        score_string += f"Scope: {len(self.scope)}, "
        score_string += f"Settebello: {self.settebello}."

        return score_string


    def calc_primiera(self):
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

        scores_denari = [card_scores[card.value] for card in self.picked_cards if card.suit == 'D']
        if len(scores_denari) == 0:
            return 0
        
        scores_bastoni = [card_scores[card.value] for card in self.picked_cards if card.suit == 'B']
        if len(scores_bastoni) == 0:
            return 0
        
        scores_coppe = [card_scores[card.value] for card in self.picked_cards if card.suit == 'C']
        if len(scores_coppe) == 0:
            return 0
        
        scores_spade = [card_scores[card.value] for card in self.picked_cards if card.suit == 'S']
        if len(scores_spade) == 0:
            return 0
        
        scores_denari.sort()
        scores_bastoni.sort()
        scores_coppe.sort()
        scores_spade.sort()

        return (scores_denari[0] + scores_bastoni[0] + 
                scores_spade[0] + scores_coppe[0])
    
class Player:
    def __init__(self, n):
        self.n = n
        self.cards = []
        self.score = Score()
        self.currently_playing = False

    def __repr__(self):
        return f"Player: [n = {self.n}, cards = {self.cards}, score = {self.score}]"
        #return f"Player: [n = {self.n}, currently_playing = {self.currently_playing}, cards = {self.cards}"

    def has_cards(self):
        return len(self.cards) > 0

    def set_cards(self, cards):
        self.cards = cards

    def is_playing(self):
        return self.currently_playing
    
    def set_playing(self):
        self.currently_playing = True

    def stop_playing(self):
        self.currently_playing = False

    def get_score(self):
        return self.score

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
    
class NetworkPlayer():
    def __init__(self, hostaddr, port):
        self.host = hostaddr
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        self.cards = []
        self.player = Player(1)

    def __repr__(self):
        return str(self.player)

    def handle_connection(self):
        msg = self.socket.recv(1024).decode()
        if msg == "":
            self.socket.close()
            self.socket = None
            return

        cmd = msg[0:4]
        payload = msg[4:]
        print(f"\n\n[DEBUG] received: cmd={cmd}, payload={payload}")
        match cmd:
            case "GETN":
                n_cards = len(self.player.cards)
                print(f"[DEBUG] answering: {str(n_cards)}")
                self.socket.sendall(str(n_cards).encode())
            case "SETC":
                received_cards = self.deserialize_cards(payload)
                print(f"[DEBUG] received cards: {received_cards}")
                self.player.set_cards(received_cards)
                self.socket.sendall(b'SETC OK')
            case "PLAY":
                upcards = self.deserialize_cards(payload)
                print(f"[DEBUG] received upcards: {upcards[4:]}")
                self.play_card(upcards)
            case "LAST":
                received_cards = self.deserialize_cards(payload)
                print(f"[DEBUG] received last cards: {received_cards}")
                self.player.set_cards(received_cards)
                self.socket.sendall(b'LAST OK')

        
        #input("Premere un tasto per continuare...")

    def play_card(self, upcards):
        print(f"[DEBUG] self.player.cards: {self.player.cards}")
        played_card, picked_cards = self.player.play_card(upcards)

        print(f"playing cards: {played_card}")
        print(f"picking cards: {picked_cards}")


        serialized_played_card = self.serialize_cards([played_card])
        serialized_picked_cards = self.serialize_cards(picked_cards)
        serialized_cards = serialized_played_card + '@' + serialized_picked_cards

        print(f"[DEBUG] sending msg: {serialized_cards}")

        self.socket.sendall(serialized_cards.encode())

    def serialize_cards(self, cards) -> str:
        msg = ''
        if cards != None:
            msg += (str((len(cards)) + 10))
            for card in cards:
                msg += str(card.value + 10)
                msg += str(ord(card.suit))
            
        return msg
    
    def deserialize_cards(self, serialized_cards):
        print(f"[DEBUG] received serialized cards from server: {serialized_cards}")
        received_cards = []
        cards_number = int(serialized_cards[:2]) - 10
        serialized_cards = serialized_cards[2:]
        for i in range(cards_number):
            card_value = int(serialized_cards[:2]) - 10
            card_suit = str(chr(int(serialized_cards[2:4])))
            received_cards.append(Card(card_value, card_suit))
            serialized_cards = serialized_cards[4:]

        return received_cards

if __name__ == "__main__":
    player = NetworkPlayer("0.0.0.0", 12345)
    
    while player.socket is not None:
        print(player)
        player.handle_connection()
