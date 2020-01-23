# CLEAR


import random

from rlcard.games.tarot.utils import init_deck
from rlcard.games.tarot.alpha_and_omega.player import TarotPlayer


class TarotDealer(object):
    """ Initialize a tarot dealer class
    """

    def __init__(self):
        self.deck = init_deck()
        self.shuffle()

    def shuffle(self):
        """ Shuffle the deck
        """
        random.shuffle(self.deck)

    def deal_cards(self, player: TarotPlayer, num):
        """ Deal some cards from deck to one player

        Args:
            player (object): The object of TarotPlayer
            num (int): The number of cards to be dealed
        """
        for _ in range(num):
            player.hand.append(self.deck.pop())
