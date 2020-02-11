from typing import List

from rlcard.games.tarot.alpha_and_omega.player import TarotPlayer
from rlcard.games.tarot.bid.bid import TarotBid
from rlcard.games.tarot.utils import cards2list


class BidRound(object):

    def __init__(self, num_players: int, starting_player: int):
        """
        Initialize the bid round class
        :param num_players: (int) the number of players in game
        :param starting_player: (int) the starting player
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

    def proceed_round(self, players: List[TarotPlayer], played_bid: TarotBid) -> int:
        """
        proceed bid round with a player bid
        :param players: List of TarotPlayer competing
        :param played_bid: the TarotBid object chosen by the current_player_id
        :return: the next player to speak
        """
        player = players[self.current_player_id]
        if player.bid is None:
            player.bid = played_bid
        if played_bid.get_str() != "PASSE":
            player.bid = played_bid
            self.taking_player_id = self.current_player_id
            player.taking = True
        if played_bid.get_str() == "PASSE":
            player.bid = played_bid
            player.taking = False

        self.max_bid_order = max(self.max_bid_order, played_bid.get_bid_order())
        self.max_bid = self.all_bids[self.max_bid_order]

        total_surrendered_players = 0
        for player_id in range(self.num_players):
            if players[player_id].bid is not None and players[player_id].bid.get_str() == "PASSE":
                total_surrendered_players += 1

        # Maximal bid encountered
        # TODO REMOVE CONSTRAINTS THAT FORCE ONLY PASSE OU PETITE (2)
        if self.max_bid_order >= 1 or (
                total_surrendered_players == self.num_players - 1 and self.taking_player_id is not None):
            for player_id in range(self.num_players):
                if player_id != self.taking_player_id:
                    players[player_id].taking = False
            self.is_over = True
        elif total_surrendered_players == self.num_players:
            self.is_dead = True
            return self.current_player_id

        # Define next speaking player within those that have not passed yet
        potential_next = (self.current_player_id + 1) % self.num_players
        if players[potential_next].bid is None:
            return potential_next
        else:
            while players[potential_next].bid.get_str() == 'PASSE':
                potential_next = (potential_next + 1) % self.num_players
            return potential_next

    def get_legal_actions(self) -> List[TarotBid]:
        # TODO REMOVE CONSTRAINTS THAT FORCE ONLY PASSE OU PETITE
        """
        Get legal bids
        :return: list of legals bids (TarotBid objects)
        """
        # legal_bids = self.all_bids[(self.max_bid_order + 1):] + [self.all_bids[0]]
        legal_bids = self.all_bids[(self.max_bid_order + 1):2] + [self.all_bids[0]]
        return legal_bids

    def get_state(self, players: List[TarotPlayer], player_id) -> dict:
        """
        Get player's state in the bid round
        :param players: list of TarotPlayer
        :param player_id: The id of the player
        :return: (dict) Dictionary containing :

                (List[str]) - hand: The list of cards in the player_id hand, with their string representation
                (int) - max_bid: the maximal bid done up to now
                (TarotBid) - current_personal_bid: current bid from the player_id
                (List[TarotBid]) - legal_actions: all legal bids that can be said by player_id
                (List[TarotBid]) - other_bids: all the other bids from other players
        """
        player = players[player_id]
        state = {'hand': cards2list(player.hand), 'max_bid': self.max_bid_order,
                 'current_personal_bid': player.bid,
                 'legal_actions': self.get_legal_actions()}
        other_bids = []
        for player in players:
            if player.player_id != player_id and player.bid is not None:
                other_bids.append(player.bid)
        state['other_bids'] = other_bids
        return state
