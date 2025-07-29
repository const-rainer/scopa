from deck import Deck 

class ScopaLoc:
    def __init__(self, players):
        self.__players = players

    def __get_n_cards(self, player):
        n_carte = len(player.get_cards())
        return n_carte

    def __set_cards(self, player, cards):
        player.set_cards(cards)

    def __get_played_cards(self, player, upcards):
        played_card, picked_cards = player.play_card(upcards)
        return played_card, picked_cards

    def __send_last_cards(self, player, cards):
        player.add_to_score(cards)

    def __terminate_game(self):
        print("\n\n ***** FINAL SCORE ***** ")
        for player in self.__players:
            print(f"{player}")

    def play_game(self):
        game_deck = Deck()
        game_deck.shuffle()
        round_n = 1

        for player in self.__players:
            cards = game_deck.get_cards(3)
            self.__set_cards(player, cards)

        upcards = game_deck.get_cards(4)

        current_player = self.__players[0]
        other_player = self.__players[1]

        last_to_pick = None

        print(f"\n\n\n----------- ROUND {round_n} -----------")

        # main loop
        while True:
            print(player)
            print(f"upcards: {upcards}")
            player_cards = self.__get_n_cards(current_player)

            if player_cards == 0 and game_deck.is_empty():
                print(f"{current_player} has 0 cards and deck is empty. The game is over")
                break

            if player_cards == 0 and not game_deck.is_empty():
                print(f"\n\n\n----------- ROUND {round_n} -----------")
                round_n += 1
                self.__set_cards(current_player, game_deck.get_cards(3))
                self.__set_cards(other_player, game_deck.get_cards(3))

            played_card, picked_cards = self.__get_played_cards(current_player, upcards)
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

        self.__send_last_cards(last_to_pick, upcards)
        upcards.clear()

        self.__terminate_game()