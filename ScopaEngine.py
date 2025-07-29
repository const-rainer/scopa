from deck import Deck 
from scopalocalplayer import ScopaLocalPlayer
from scopanetworkplayer import ScopaNetworkPlayer
from scopaloc import ScopaLoc
from scopaserv import ScopaServ

class ScopaEngine:
    def __init__(self, host=None, port=None):
        if host is None or port is None:
            self.__players = [ScopaLocalPlayer(1), ScopaLocalPlayer(2)]
            self.__server = ScopaLoc()
        else:
            self.__server = ScopaServ(host, port)
            self.__players = []
            while len(self.__players) < 2:
                conn, addr = self.__server.server_socket.accept()
                self.__players.append(conn)
                print(f"[Player connected] address: {addr[0]}, port: {addr[1]}")

        print("\n--- [Players connected. Starting game.] ---\n")

    def play_game(self):
        game_deck = Deck()
        game_deck.shuffle()
        round_n = 1

        for player in self.__players:
            cards = game_deck.get_cards(3)
            self.__server.set_cards(player, cards)

        upcards = game_deck.get_cards(4)

        current_player = self.__players[0]
        other_player = self.__players[1]

        last_to_pick = None

        print(f"\n\n\n----------- ROUND {round_n} -----------")

        # main loop
        while True:
            print(player)
            print(f"upcards: {upcards}")
            player_cards = self.__server.get_n_cards(current_player)

            if player_cards == 0 and game_deck.is_empty():
                print(f"{current_player} has 0 cards and deck is empty. The game is over")
                break

            if player_cards == 0 and not game_deck.is_empty():
                print(f"\n\n\n----------- ROUND {round_n} -----------")
                round_n += 1
                self.__server.set_cards(current_player, game_deck.get_cards(3))
                self.__server.set_cards(other_player, game_deck.get_cards(3))

            played_card, picked_cards = self.__server.get_played_cards(current_player, upcards)
            if picked_cards is None:
                upcards.append(played_card)
            else:
                if picked_cards == upcards:
                    print("SCOPA!!")

                print(f"[DEBUG] Removing {picked_cards} from upcards")
                for card in picked_cards:
                    upcard_to_remove = next((u for u in upcards if u.value == card.value and u.suit == card.suit), None)
                    upcards.remove(upcard_to_remove)
                    last_to_pick = current_player

            current_player, other_player = other_player, current_player
            print("")

        self.__server.send_last_cards(last_to_pick, upcards)
        upcards.clear()

        self.__server.terminate_game(self.__players)
        

if __name__ == "__main__":
    eng = ScopaEngine(host="0.0.0.0", port=12345)
    #eng = ScopaEngine()
    eng.play_game()