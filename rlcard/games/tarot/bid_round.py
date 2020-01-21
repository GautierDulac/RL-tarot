from rlcard.games.tarot.bid import TarotBid
from rlcard.games.tarot.player import TarotPlayer
from typing import List


class BidRound(object):

    def __init__(self, num_players):
        """ Initialize the bid round class

        Args:
            num_players (int): the number of players in game
        """
        self.current_player_id = 0
        self.num_players = num_players
        self.direction = 1
        self.max_bid = None
        self.is_over = False
        self.taker = None
        self.all_bids = [TarotBid('PASSE'),
                         TarotBid('PETITE'),
                         TarotBid('POUSSE'),
                         TarotBid('GARDE'),
                         TarotBid('GARDE_SANS'),
                         TarotBid('GARDE_CONTRE')]

    def proceed_round(self, players: List[TarotPlayer], played_bid: TarotBid):
        """ proceed bid round with a player bid

        Args:
            :param played_bid: TarotBid
            :param players: list of object of TarotPlayer
        """
        player = players[self.current_player_id]
        player.bid.append(played_bid)

        self.max_bid = played_bid.get_bid_order()

    def get_legal_bids(self):
        """
        Get legal bids
        :return: list of legals bids
        """
        legal_bids = self.all_bids[(self.max_bid + 1):]

        return legal_bids

    def get_bid_state(self, players: List[TarotPlayer], player_id):
        """ Get player's state in the bid round

        Args:
            :param player_id: The id of the player
            :param players: list of TarotPlayer
        """
        state = {}
        player = players[player_id]
        state['max_bid'] = self.max_bid
        state['current_personnal_bid'] = player.bid
        other_bids = []
        for player in players:
            if player.player_id != player_id:
                other_bids.extend(player.bid)
        state['other_bids'] = other_bids
        state['legal_actions'] = self.get_legal_bids()
        return state
