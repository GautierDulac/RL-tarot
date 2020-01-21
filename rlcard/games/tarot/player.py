# CLEAR


class TarotPlayer(object):

    def __init__(self, player_id, taking=False):
        """ Initilize a player.

        Args:
            player_id (int): The id of the player
        """
        self.player_id = player_id
        self.hand = []
        self.points = []
        self.bouts = []
        self.bid = []
        self.taking = taking

    def get_player_id(self):
        """ Return the id of the player
        """

        return self.player_id
