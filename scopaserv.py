import socket
from card import Card

class ScopaServ():
    def __init__(self, host, port):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen(2)

        print(f"[ScopaServ listening on address {host}:{port}]")

    def get_n_cards(self, player):
        msg = "GETN"
        print(f"[DEBUG] sending {msg} to player {player.fileno()}")
        player.sendall(msg.encode())

        n_carte = int(player.recv(16).decode())
        print(f"[DEBUG] received: {n_carte}")

        return n_carte

    def set_cards(self, player, cards):
        serialized_cards = self.__serialize_cards(cards)
        msg = "SETC" + serialized_cards
        print(f"[DEBUG] sending {msg} to player {player.fileno()}")
        player.sendall(msg.encode())

        reply = player.recv(16).decode()
        print(f"[DEBUG] received {reply}")

    def get_played_cards(self, player, upcards):
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
    
    def send_last_cards(self, player, cards):
        serialized_cards = self.__serialize_cards(cards)
        msg = "LAST" + serialized_cards
        print(f"[DEBUG] sending {msg} to player {player.fileno()}")
        player.sendall(msg.encode())

        reply = player.recv(1024).decode()
        print(f"[DEBUG] received {reply}")

    def terminate_game(self, clients):
        for c in clients:
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