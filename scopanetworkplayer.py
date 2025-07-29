import random
import socket
from card import Card
from deck import Deck
from player import Player
from typing import List

class ScopaNetworkPlayer():
    def __init__(self, host, port):
        self.__player : Player = None
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket.connect((host, port))

    def __repr__(self):
        return str(self.__player)

    def set_player(self, player : Player):
        self.__player = player

    def start(self):
        while self.__socket is not None:
            print(self.__player)
            self.__handle_connection()

    '''
        This method handles the communication with the server. 
        The server always initiates the communications by sending a message in the form <CMD><PAYLOAD>.

        The received message is decoded and a different action is performed depending on the command, 
        which is stored in the first 4 bytes of the message.

        Available commands:
        GETN: Asks how many cards the player has. The player replies with the number.
        SETC: Gives cards to the player. The payload contains the new cards. The player 
                stores the cards and replies with a status message.
        PLAY: Asks the player to play a card. The payload contains the current upcards.
                The player replies with a message containing the card it has played and 
                the cards it has picked (if any). The information is encoded in the form
                <played_card>@<picked_cards>.
        LAST: Gives the player the last upcards remaining on the table after the match 
                is over. The player stores the cards and replies with a status message.
    '''
    def __handle_connection(self):
        msg = self.__socket.recv(1024).decode()
        
        if msg == "":
            self.__socket.close()
            self.__socket = None
            return
        
        cmd = msg[0:4]
        payload = msg[4:]
        print(f"\n\n[DEBUG] received: cmd={cmd}, payload={payload}")

        match cmd:
            case "GETN":
                n_cards = len(self.__player.get_cards())
                print(f"[DEBUG] answering: {str(n_cards)}")
                self.__socket.sendall(str(n_cards).encode())

            case "SETC":
                received_cards = self.__deserialize_cards(payload)
                print(f"[DEBUG] received cards: {received_cards}")
                self.__player.set_cards(received_cards)
                self.__socket.sendall(b'SETC OK')

            case "PLAY":
                upcards = self.__deserialize_cards(payload)
                print(f"[DEBUG] received upcards: {upcards}")
                self.__play_card(upcards)

            case "LAST":
                received_cards = self.__deserialize_cards(payload)
                print(f"[DEBUG] received last cards: {received_cards}")
                self.__player.add_to_score(received_cards)
                self.__socket.sendall(b'LAST OK')

    def __play_card(self, upcards : List[Card]):
        print(f"[DEBUG] self.__player.cards: {self.__player.cards}")

        played_card, picked_cards = self.__player.play_card(upcards)
        print(f"playing cards: {played_card}")
        print(f"picking cards: {picked_cards}")

        self.__send_cards(played_card, picked_cards)

    def __send_cards(self, played_card : Card, picked_cards : List[Card]):
        serialized_played_card = self.__serialize_cards([played_card])
        serialized_picked_cards = self.__serialize_cards(picked_cards)
        serialized_cards = serialized_played_card + '@' + serialized_picked_cards

        print(f"[DEBUG] sending msg: {serialized_cards}")
        self.__socket.sendall(serialized_cards.encode())

    def __serialize_cards(self, cards : List[Card]) -> str:
        msg = ''
        if cards != None:
            msg += (str((len(cards)) + 10))
            for card in cards:
                msg += str(card.value + 10)
                msg += str(ord(card.suit))
            
        return msg
    
    def __deserialize_cards(self, serialized_cards : str) -> List[Card]: 
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
    network_player = ScopaNetworkPlayer("0.0.0.0", 12345)
    network_player.set_player(Player(1))
    
    network_player.start()
