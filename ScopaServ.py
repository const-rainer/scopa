import socket
import random
import logging
from card import Card
from deck import Deck

logger = logging.getLogger()

class ScopaServ():
    def __init__(self, host, port):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen(2)

        print(f"[ScopaServ listening on address {host}:{port}]")

        self.clients = []
        self.addresses = []

    def __get_n_cards(self, player):
        msg = "GETN"
        print(f"[DEBUG] sending {msg} to player {player.fileno()}")
        player.sendall(msg.encode())

        n_carte = int(player.recv(16).decode())
        print(f"[DEBUG] received: {n_carte}")

        return n_carte

    def __set_cards(self, player, cards):
        serialized_cards = self.__serialize_cards(cards)
        msg = "SETC" + serialized_cards
        print(f"[DEBUG] sending {msg} to player {player.fileno()}")
        player.sendall(msg.encode())

        reply = player.recv(16).decode()
        print(f"[DEBUG] received {reply}")

    def __get_played_cards(self, player, upcards):
        serialized_upcards = self.__serialize_cards(upcards)
        msg = "PLAY" + serialized_upcards
        print(f"[DEBUG] sending {msg} to player {player.fileno()}")
        player.sendall(msg.encode())

        received_cards = player.recv(1024).decode()
        played_card, picked_cards = self.__deserialize_cards(received_cards)
        #print(f"[DEBUG] received cards:")
        #print(f"[DEBUG] played_card: {played_card}")
        #print(f"[DEBUG] picked_cards: {picked_cards}")

        return played_card, picked_cards
    
    def __send_last_cards(self, player, cards):
        serialized_cards = self.__serialize_cards(cards)
        msg = "LAST" + serialized_cards
        print(f"[DEBUG] sending {msg} to player {player.fileno()}")
        player.sendall(msg.encode())

        reply = player.recv(1024).decode()
        print(f"[DEBUG] received {reply}")

    def start(self):
        while len(self.clients) < 2:
            conn, addr = self.server_socket.accept()
            self.clients.append(conn)
            self.addresses.append(addr)
            print(f"[Player connected] address: {addr[0]}, port: {addr[1]}")

        print("\n--- [Players connected. Starting game.] ---\n")

        game_deck = Deck()
        game_deck.shuffle()
        cards_left = 40
        round_n = 1

        for player in self.clients:
            cards = game_deck.get_cards(3)
            self.__set_cards(player, cards)

        upcards = game_deck.get_cards(4)

        current_player = self.clients[0]
        other_player = self.clients[1]

        last_to_pick = None

        print(f"\n\n\n----------- ROUND {round_n} -----------")

        while cards_left > 0:
            print(f"current player: {current_player.fileno()}")
            print(f"upcards: {upcards}")
            player_cards = self.__get_n_cards(current_player)
            
            if player_cards == 0 and game_deck.is_empty():
                print(f"Player {current_player.fileno()} has 0 cards and deck is empty. The game is over")
                break
            
            if player_cards == 0 and not game_deck.is_empty():
                print(f"\n\n\n----------- ROUND {round_n} -----------")
                round_n += 1
                self.__set_cards(current_player, game_deck.get_cards(3))
                self.__set_cards(other_player, game_deck.get_cards(3))
    
            played_card, picked_cards = self.__get_played_cards(current_player, upcards)
            print(f"[DEBUG] player {current_player.fileno()} played: {played_card}. Picks: {picked_cards}.")
            if picked_cards is None:
                upcards.append(played_card)
            else:
                if picked_cards == upcards:
                    print("SCOPA!!")
                cards_left -= len(picked_cards) + 1
                print(f"[DEBUG] Removing {picked_cards} from upcards")
                for card in picked_cards:
                    upcard_to_remove = next((u for u in upcards if u.value == card.value and u.suit == card.suit), None)
                    upcards.remove(upcard_to_remove)
                    last_to_pick = current_player

            current_player, other_player = other_player, current_player
            print("")

        self.__send_last_cards(last_to_pick, upcards)
        upcards.clear()

        for c in self.clients:
            c.shutdown(socket.SHUT_RDWR)
            c.close()
        self.server_socket.shutdown(socket.SHUT_RDWR)
        self.server_socket.close()

    def __serialize_cards(self, cards) -> str:
        msg = ''
        if cards != None:
            msg += (str((len(cards)) + 10))
            for card in cards:
                msg += str(card.value + 10)
                msg += str(ord(card.suit))
            
        return msg
    
    def __deserialize_cards(self, serialized_cards):
        received_cards = serialized_cards.split('@')
        print(f"[DEBUG] received_cards = {received_cards}")

        encoded_played_card = received_cards[0][2:]
        played_card_value = int(encoded_played_card[:2]) - 10
        played_card_suit = str(chr(int(encoded_played_card[2:4])))
        
        played_card = Card(played_card_value, played_card_suit)

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