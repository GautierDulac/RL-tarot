# CLEAR
from rlcard.games.tarot.alpha_and_omega.player import TarotPlayer


class TarotDog(TarotPlayer):

    def __init__(self, player_id=None):
        """ Initilize the dog as a player.
        """
        super().__init__(player_id)
        self.hand = []
