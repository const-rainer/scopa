import socket
import random
import copy
import logging

logger = logging.getLogger()

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
            for suit in ['B', 'C', 'D', 'S']
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

class ScopaServ():
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(2)

        print(f"[ScopaServ listening on address {self.host}:{self.port}]")

        self.clients = []
        self.addresses = []

    def quante_carte(self, player):
        msg = "GETN"
        print(f"[DEBUG] sending {msg} to player")
        player.sendall(msg.encode())
        n_carte = int(player.recv(16).decode())
        print(f"[DEBUG] ricevuto: {n_carte}")
        return n_carte

    def servo_carte(self, player, cards):
        print(f"Servo carte al giocatore {player}")
        serialized_cards = self.serialize_cards(cards)
        msg = "SETC" + serialized_cards

        print(f"[DEBUG] sending {msg}")
        
        player.sendall(msg.encode())
        reply = player.recv(16).decode()
        if reply == "SETC OK":
            print(f"[DEBUG] player replied {reply}")
        else:
            print(f"Error: received msg {reply}")

    def get_played_cards(self, player, upcards):
        serialized_upcards = self.serialize_cards(upcards)
        msg = "PLAY" + serialized_upcards
        print(f"[DEBUG] sending {msg}")
        player.sendall(msg.encode())
        received_cards = player.recv(1024).decode()
        print(f"[DEBUG] received_cards from client: {received_cards}")
        played_card, picked_cards = self.deserialize_cards(received_cards)

        print(f"[DEBUG] received cards:")
        print(f"[DEBUG] played_card: {played_card}")
        print(f"[DEBUG] picked_cards: {picked_cards}")

        return played_card, picked_cards

    def start(self):
        while len(self.clients) < 2:
            conn, addr = self.server_socket.accept()
            self.clients.append(conn)
            self.addresses.append(addr)
            print(f"[Player connected] address: {addr[0]}, port: {addr[1]}")

        print("\n--- [Players connected. Starting game.] ---\n")

        deck = Deck()
        deck.shuffle()
        print(f"[DEBUG] Numero carte: {deck}")
        cards_left = 40
        round_n = 1

        for player in self.clients:
            cards = deck.get_cards(3)
            self.servo_carte(player, cards)

        upcards = deck.get_cards(4)

        current_player = self.clients[0]
        other_player = self.clients[1]

        while cards_left > 0:
            print(f"Round: {round_n}, Cards left: {cards_left}, upcards: {upcards}")
            print(f"Cards left: {cards_left}")
            print(f"current player: {current_player.fileno()}")
            player_cards = self.quante_carte(current_player)
            if player_cards == 0:
                print(f"Player ha {player_cards} carte.")
                cards = deck.get_cards(3)
                self.servo_carte(current_player, cards)
    
            played_card, picked_cards = self.get_played_cards(current_player, upcards)
            if picked_cards is None:
                upcards.append(played_card)
            else:
                cards_left -= len(picked_cards)
                for card in picked_cards:
                    print(f"[DEBUG] trying to remove card {card} from upcards")
                    upcard_to_remove = next((u for u in upcards if u.value == card.value and u.suit == card.suit), None)
                    upcards.remove(upcard_to_remove)

            current_player, other_player= other_player, current_player

    def serialize_cards(self, cards) -> str:
        msg = ''
        if cards != None:
            msg += (str((len(cards)) + 10))
            for card in cards:
                msg += str(card.value + 10)
                msg += str(ord(card.suit))
            
        return msg
    
    def deserialize_cards(self, serialized_cards):
        print(f"[DEBUG] serialized_cards = {serialized_cards}")
        received_cards = serialized_cards.split('@')
        print(f"[DEBUG] received_cards = {received_cards}")

        encoded_played_card = received_cards[0][2:]
        played_card_value = int(encoded_played_card[:2]) - 10
        print(f"[DEBUG] played_card_value = {played_card_value}")

        played_card_suit = str(chr(int(encoded_played_card[2:4])))
        print(f"[DEBUG] played_card_suit = {played_card_suit}")
        
        played_card = Card(played_card_value, played_card_suit)
        print(f"[DEBUG] played_card = {played_card}")

        encoded_picked_cards = received_cards[1]
        if len(encoded_picked_cards) == 0:
            return played_card, None

        picked_cards = []
        cards_number = int(encoded_picked_cards[:2]) - 10
        encoded_picked_cards = encoded_picked_cards[2:]

        for i in range(cards_number):
            card_value = int(encoded_picked_cards[:2]) - 10
            card_suit = str(chr(int(encoded_picked_cards[2:4])))
            picked_cards.append(Card(card_value, card_suit))
            encoded_picked_cards = encoded_picked_cards[4:]

        return played_card, picked_cards
    

if __name__ == "__main__":
    scopaserv = ScopaServ("0.0.0.0", 12345)
    scopaserv.start()