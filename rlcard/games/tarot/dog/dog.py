from rlcard.games.tarot.alpha_and_omega.player import TarotPlayer
from rlcard.games.tarot.utils import get_pot_value


class TarotDog(TarotPlayer):

    def __init__(self, player_id: int = None):
        """
        Initialize the dog as a player
        :param player_id: No id required here, but required for upper class TarotPlayer
        """
        super().__init__(player_id)
        self.hand = []

    def get_points_in_dog(self) -> float:
        """
        Compute points in the dog using the function get_pot_value from utils
        :return: float number of points
        """
        return get_pot_value(self.hand)
