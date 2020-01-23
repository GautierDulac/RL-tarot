from rlcard.games.tarot.bid.bid import TarotBid
from rlcard.games.tarot.alpha_and_omega.player import TarotPlayer
from rlcard.games.tarot.utils import cards2list
from typing import List


class BidRound(object):

    def __init__(self, num_players, starting_player):
        """ Initialize the bid round class

        Args:
            num_players (int): the number of players in game
        """
        self.current_player_id = starting_player
        self.num_players = num_players
        self.direction = 1
        self.max_bid = 0
        self.is_over = False
        self.is_dead = False
        self.taking = None
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
        if len(player.bid) == 0:
            player.bid.append(played_bid)
        elif player.bid[-1].bid != "PASSE":
            player.bid.append(played_bid)

        self.max_bid = max(self.max_bid, played_bid.get_bid_order())

        total_surrendered_players = 0
        for player_id in range(self.num_players):
            if players[player_id].bid[-1].bid == "PASSE":
                total_surrendered_players += 1
                players[player_id].taking = False
            else:
                players[player_id].taking = True

        # Maximal bid encountered
        if self.max_bid == 5:
            self.is_over = True
        elif total_surrendered_players == self.num_players - 1:
            self.is_over = True
        elif total_surrendered_players == self.num_players:
            self.is_dead = True

        return (self.current_player_id + 1) % self.num_players

    def get_legal_actions(self):
        """
        Get legal bids
        :return: list of legals bids
        """
        legal_bids = self.all_bids[(self.max_bid + 1):] + [self.all_bids[0]]

        return legal_bids

    def get_state(self, players: List[TarotPlayer], player_id):
        # TODO : Check relevance of this state for bid round
        """ Get player's state in the bid round

        Args:
            :param player_id: The id of the player
            :param players: list of TarotPlayer
        """
        state = {}
        player = players[player_id]
        state['hand'] = cards2list(player.hand)
        state['max_bid'] = self.max_bid
        state['current_personnal_bid'] = player.bid
        other_bids = []
        for player in players:
            if player.player_id != player_id:
                other_bids.extend(player.bid)
        state['other_bids'] = other_bids
        state['legal_actions'] = self.get_legal_actions()
        return state