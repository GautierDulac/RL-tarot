from typing import List

from rlcard.games.tarot.alpha_and_omega.dealer import TarotDealer as Dealer
from rlcard.games.tarot.alpha_and_omega.player import TarotPlayer
from rlcard.games.tarot.bid.bid import TarotBid
from rlcard.games.tarot.bid.bid_round import BidRound
from rlcard.games.tarot.dog.dog import TarotDog


class BidGame(object):

    def __init__(self, players: List[TarotPlayer], num_players: int, starting_player: int, num_cards_per_player: int,
                 num_cards_dog: int,
                 dog: TarotDog):
        self.num_players = num_players
        self.num_cards_per_player = num_cards_per_player
        self.num_cards_dog = num_cards_dog
        self.starting_player = starting_player
        # Initialize a dealer that can deal cards
        self.dealer = None
        # Initialize four players to play the game
        self.players = players
        # Initialize the Dog
        self.dog = dog
        # Initialize a Bid Round instance
        self.bid_round = None
        # Bid round over ?
        self.bid_over = False
        # Taking player ?
        self.taking_player_id = None
        self.taking_bid_order = None

    def init_game(self) -> (dict, int):
        """
        Initialize players and state for bid game
        :return:
        (tuple): Tuple containing:

                (dict): The first state in one game
                (int): Current bidder's id
        """
        # Initialize bid Round
        self.bid_round = BidRound(self.num_players, self.starting_player)

        # Deal 18 cards to each player to prepare for the game
        self.dealer = Dealer()
        for player in self.players:
            player.hand = []
            self.dealer.deal_cards(player, self.num_cards_per_player)

        # Deal 6 cards to the dog
        self.dealer.deal_cards(self.dog, self.num_cards_dog)

        player_id = self.bid_round.current_player_id
        state = self.get_state(player_id)

        return state, player_id

    def step(self, played_bid: TarotBid) -> (dict, int):
        """
        Get the next state
        :param played_bid: a TarotBid object chosen to be saif by the current player
        :return:
        (tuple): Tuple containing:

                (dict): next player's state
                (int): next plater's id
        """
        player_id = self.bid_round.proceed_round(self.players, played_bid)
        if self.bid_round.is_dead:
            return None, None
        elif self.bid_round.is_over:
            self.bid_over = True
            self.taking_player_id = self.bid_round.taking_player_id
            self.taking_bid_order = self.bid_round.max_bid_order
            return self.get_state(player_id), player_id
        else:
            state = self.get_state(player_id)
            self.bid_round.current_player_id = player_id
            return state, player_id

    def get_state(self, player_id: int) -> dict:
        """
        Return player's state
        :param player_id: (int) player id
        :return: (dict) The state of the player
        """
        state = self.bid_round.get_state(self.players, player_id)
        return state

    def get_legal_actions(self) -> List[TarotBid]:
        """
        Return the legal actions for current player
        :return: (list): A list of legal actions (TarotBid objects)
        """
        return self.bid_round.get_legal_actions()

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
        :return: (int): The number of actions. There are 6 actions during BID game part
        """
        return 6

    def get_player_id(self) -> int:
        """
        Return the current player's id
        :return: (int): current player's id
        """
        return self.bid_round.current_player_id

    def is_over(self) -> bool:
        """
        Check if the game is over
        :return: (boolean): True if the game is over
        """
        return self.bid_round.is_over
