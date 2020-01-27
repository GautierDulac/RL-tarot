from rlcard.games.tarot.bid.bid import TarotBid
from rlcard.games.tarot.alpha_and_omega.player import TarotPlayer
from rlcard.games.tarot.utils import cards2list
from typing import List

import random

random.seed(43)  # TODO REMOVE


class BidRound(object):

    def __init__(self, num_players, starting_player):
        """ Initialize the bid round class

        Args:
            num_players (int): the number of players in game
        """
        self.current_player_id = starting_player
        self.num_players = num_players
        self.direction = 1
        self.max_bid_order = 0
        self.is_over = False
        self.is_dead = False
        self.taking_player_id = None
        self.all_bids = [TarotBid('PASSE'),
                         TarotBid('PETITE'),
                         TarotBid('POUSSE'),
                         TarotBid('GARDE'),
                         TarotBid('GARDE_SANS'),
                         TarotBid('GARDE_CONTRE')]
        self.max_bid = self.all_bids[self.max_bid_order]

    def proceed_round(self, players: List[TarotPlayer], played_bid: TarotBid):
        """ proceed bid round with a player bid

        Args:
            :param played_bid: TarotBid
            :param players: list of object of TarotPlayer
        """
        player = players[self.current_player_id]
        if player.bid is None:
            player.bid = played_bid
        if player.bid.get_str() != "PASSE":
            player.bid = played_bid
            self.taking_player_id = self.current_player_id

        self.max_bid_order = max(self.max_bid_order, played_bid.get_bid_order())
        self.max_bid = self.all_bids[self.max_bid_order]

        total_surrendered_players = 0
        for player_id in range(self.num_players):
            if players[player_id].bid is not None and players[player_id].bid.get_str() == "PASSE":
                total_surrendered_players += 1
                players[player_id].taking = False
            else:
                players[player_id].taking = True

        # Maximal bid encountered
        if self.max_bid_order == 5:
            for player_id in range(self.num_players):
                if player_id != self.current_player_id:
                    players[player_id].taking = False
            self.taking_player_id = self.current_player_id
            self.is_over = True
        elif total_surrendered_players == self.num_players - 1:
            if self.taking_player_id is not None:
                self.is_over = True
        elif total_surrendered_players == self.num_players:
            self.is_dead = True

        # Define next speaking player within those that have not passed yet
        potential_next = (self.current_player_id + 1) % self.num_players
        if players[potential_next].bid is None:
            return potential_next
        else:
            while players[potential_next].bid.get_str() == 'PASSE':
                potential_next = (potential_next + 1) % self.num_players
            return potential_next

    def get_legal_actions(self):
        """
        Get legal bids
        :return: list of legals bids
        """
        legal_bids = self.all_bids[(self.max_bid_order + 1):] + [self.all_bids[0]]

        return legal_bids

    def get_state(self, players: List[TarotPlayer], player_id):
        """ Get player's state in the bid round

        Args:
            :param player_id: The id of the player
            :param players: list of TarotPlayer
        """
        player = players[player_id]
        state = {'hand': cards2list(player.hand), 'max_bid': self.max_bid_order,
                 'current_personnal_bid': player.bid,
                 'legal_actions': self.get_legal_actions()}
        other_bids = []
        for player in players:
            if player.player_id != player_id and player.bid is not None:
                other_bids.append(player.bid)
        state['other_bids'] = other_bids
        return state
