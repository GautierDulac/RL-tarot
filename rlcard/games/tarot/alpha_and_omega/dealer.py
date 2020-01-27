import random

from rlcard.games.tarot.utils import init_deck
from rlcard.games.tarot.alpha_and_omega.player import TarotPlayer


class TarotDealer(object):
    """ Initialize a tarot dealer class
    """

    def __init__(self):
        """
        Initialize a TarotDealer object
        """
        self.deck = init_deck()
        self.shuffle()

    def shuffle(self):
        """
        Shuffle the deck
        :return: No return, directly modify the deck
        """
        random.shuffle(self.deck)

    def deal_cards(self, player: TarotPlayer, num: int):
        """
        Deal some cards from deck to one player
        :param player: The player whom to deal cards
        :param num: Number of card to be given
        :return: No return - directly modify player
        """
        for _ in range(num):
            player.hand.append(self.deck.pop())
