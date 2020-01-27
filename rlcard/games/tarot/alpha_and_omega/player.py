class TarotPlayer(object):

    def __init__(self, player_id: int):
        """
        Initialize a TarotPlayer object
        :param player_id: int
        """
        self.player_id = player_id
        self.hand = []
        self.points = 0
        self.bouts = 0
        self.bid = None
        self.taking = False

    def get_player_id(self):
        """ Return the id of the player
        """

        return self.player_id
