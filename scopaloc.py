class ScopaLoc:
    def get_n_cards(self, player):
        n_carte = len(player.get_cards())
        return n_carte

    def set_cards(self, player, cards):
        player.set_cards(cards)

    def get_played_cards(self, player, upcards):
        played_card, picked_cards = player.play_card(upcards)
        return played_card, picked_cards

    def send_last_cards(self, player, cards):
        player.add_to_score(cards)

    def terminate_game(self, players):
        print("\n\n ***** FINAL SCORE ***** ")
        for player in players:
            print(f"{player}")

    