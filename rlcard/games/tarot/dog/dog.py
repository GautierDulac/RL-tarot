# CLEAR
from rlcard.games.tarot.alpha_and_omega.player import TarotPlayer
from rlcard.games.tarot.utils import get_pot_value


class TarotDog(TarotPlayer):

    def __init__(self, player_id=None):
        """ Initilize the dog as a player.
        """
        super().__init__(player_id)
        self.hand = []

    def get_points_in_dog(self):
        """

        :return:
        """
        return get_pot_value(self.hand)
