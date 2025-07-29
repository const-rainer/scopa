from card import Card
from typing import List

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

        self.__update_score()

    def add_last_cards(self, last_cards):
        self.picked_cards.extend(last_cards)
        self.__update_score()

    def __update_score(self):
        if not self.settebello:
            self.settebello = any(card.value == 7 and card.suit == 'D' 
                                    for card in self.picked_cards)
        
        self.primiera = self.__calc_primiera()
        self.denari = len([card for card in self.picked_cards if card.suit == 'D'])

    def __repr__(self):
        score_string = ""
        score_string += f"Carte: {len(self.picked_cards)}, "
        score_string += f"Denari: {self.denari}, "
        score_string += f"Primiera: {self.primiera}, "
        score_string += f"Scope: {len(self.scope)}, "
        score_string += f"Settebello: {self.settebello}."

        return score_string


    def __calc_primiera(self):
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