from card import Card
from deck import Deck
from itertools import combinations
from player import Player
from score import Score
import random

class ScopaLocalPlayer:
    def __init__(self, n=0):
        self.__player = Player(n)

    def __repr__(self):
        return str(self.__player)

    def set_player(self, player : Player):
        self.__player = player

    def set_cards(self, cards):
        self.__player.set_cards(cards)

    def get_cards(self):
        return self.__player.get_cards()

    def play_card(self, upcards):
        played_card, picked_cards = self.__player.play_card(upcards)
        return played_card, picked_cards

    def add_to_score(self, cards):
        self.__player.add_to_score(cards)