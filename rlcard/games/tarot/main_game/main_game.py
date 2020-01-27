from typing import List

from rlcard.games.tarot.alpha_and_omega.card import TarotCard
from rlcard.games.tarot.alpha_and_omega.player import TarotPlayer
from rlcard.games.tarot.main_game.main_round import MainRound


class MainGame(object):

    def __init__(self, num_players: int, num_cards_per_player: int, starting_player: int, players: List[TarotPlayer],
                 taking_player_id: int, new_dog: List[TarotCard]):
        """
        Initialize a MainGame object
        :param num_players: Number of players
        :param num_cards_per_player: Number of cards per player
        :param starting_player: Starting player
        :param players: List of TarotPlayers
        :param taking_player_id: Id of the player that won the BID part
        :param new_dog: List of cards in the dog (None if BID is GARDE_SANS or GARDE_CONTRE)
        """
        self.num_players = num_players
        self.num_cards_per_player = num_cards_per_player
        self.starting_player = starting_player
        self.players = players
        self.taking_player_id = taking_player_id
        self.taking_bid = self.players[self.taking_player_id].bid.get_bid_order()
        self.new_dog = new_dog
        # Initialize a Round instance
        self.main_round = None
        # End of game
        self.is_over = False
        self.payoffs = dict()
        for player_id in range(num_players):
            self.payoffs[player_id] = 0

    def init_game(self) -> (dict, int):
        """
        Initialize round and state for the game
        :return: (tuple): Tuple containing:

                (dict): The first state in one game
                (int): Current player's id
        """
        for player_id in range(self.num_players):
            self.payoffs[player_id] = 0

        # Initialize a Round
        self.main_round = MainRound(self.starting_player, self.num_players, self.num_cards_per_player, self.taking_bid,
                                    self.new_dog)

        player_id = self.main_round.current_player_id
        state = self.get_state(player_id)
        return state, player_id

    def step(self, played_card: TarotCard) -> (dict, int):
        """
        Get the next state using a specified card
        :param played_card: Chosen (TarotCard) to be played
        :return: (tuple): Tuple containing:

                (dict): next player's state
                (int): next plater's id
        """
        player_id = self.main_round.proceed_round(self.players, played_card)

        if self.main_round.is_over:
            self.is_over = True

        state = self.get_state(player_id)
        self.main_round.current_player_id = player_id
        return state, player_id

    def get_state(self, player_id: int) -> dict:
        """
        Return player's state
        :param player_id: (int) player_id
        :return: (dict): The state of the player
        """
        state = self.main_round.get_state(self.players, player_id)
        return state

    def get_payoffs(self) -> dict:
        """
        Return the payoffs of the game
        :return: (dict): Each entry corresponds to the payoff of one player
        """
        winner = self.main_round.winner

        # Counting points
        winning_points = self.players[self.taking_player_id].points
        winning_bouts = self.players[self.taking_player_id].bouts
        if winning_bouts == 0:
            asked_contract = 56
        elif winning_bouts == 1:
            asked_contract = 51
        elif winning_bouts == 2:
            asked_contract = 41
        else:  # winning_bouts == 3:
            asked_contract = 36
        additional_points = abs(int((winning_points - asked_contract) / 10))
        total_contract_points = self.players[self.taking_player_id].bid.get_bid_value() + additional_points
        # Defining sense of the final points for every one (POS is taker winner, NEG otherwise)
        if winner is not None and len(winner) == 1:
            taker_winner = 1
        else:
            taker_winner = -1
        # Giving points to the taker - SPECIFIC to a 4 player game
        self.payoffs[self.taking_player_id] = taker_winner * 3 * total_contract_points
        # Giving points to the others
        for player_id in range(self.num_players):
            if player_id != self.taking_player_id:
                self.payoffs[player_id] = - total_contract_points * taker_winner

        return self.payoffs

    def get_legal_actions(self) -> List[TarotCard]:
        """
        Return the legal actions for current player
        :return: (List[TarotCard]) list of all tarotcards that can be played
        """
        return self.main_round.get_legal_actions(self.players, self.main_round.current_player_id)

    def get_player_num(self) -> int:
        """
        Return the number of players in Tarot
        :return: (int): The number of players in the game
        """
        return self.num_players

    @staticmethod
    def get_action_num() -> int:
        """
        Return the number of applicable actions
        :return: (int): The number of actions. There are 78 actions in the main game
        """
        return 78

    def get_player_id(self) -> int:
        """
        Return the current player's id
        :return: (int): current player's id
        """
        return self.main_round.current_player_id
