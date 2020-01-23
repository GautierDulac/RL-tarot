from rlcard.games.tarot.dog.dog_round import DogRound
from rlcard.games.tarot.bid.bid import TarotBid
from rlcard.games.tarot.dog.dog import TarotDog
from rlcard.games.tarot.alpha_and_omega.player import TarotPlayer
from typing import List


class DogGame(object):

    def __init__(self, players: List[TarotPlayer], taking_player_id: int,
                 num_cards_per_player: int, num_cards_dog: int, dog: TarotDog, taking_bid: TarotBid):
        self.num_cards_per_player = num_cards_per_player
        self.num_cards_dog = num_cards_dog
        # Initialize players
        self.players = players
        self.taking_player = players[taking_player_id]
        self.current_player_id = taking_player_id
        # Initialize the dog round
        self.dog_round = DogRound(self.taking_player, taking_player_id, dog, num_cards_dog, taking_bid)
        # Get the known cards
        self.known_cards = []
        # Taking bid for the taking player
        self.taking_bid = taking_bid
        # Is over ?
        self.is_over = False

    def init_game(self):
        """ Initialize Status for Dog Round

        Returns:
            (tuple): Tuple containing:

                (dict): The first state in one game
                (int): Current bidder's id
        """
        if TarotBid.get_bid_order(self.taking_bid) >= 4:
            self.known_cards = self.taking_player.hand
        else:
            self.known_cards = self.dog_round.all_cards

        player_id = self.dog_round.taking_player_id
        state = self.get_state(player_id)

        return state, player_id

    def step(self, played_dog_card):
        """ Get the next state

        Args:
            played_dog_card (TarotCard): A specific card

        Returns:
            (tuple): Tuple containing:

                (dict): next player's state
                (int): next plater's id
        """

        player_id = self.dog_round.proceed_round(self.players, played_dog_card)

        if self.dog_round.is_over:
            self.is_over = True

        state = self.get_state(player_id)
        return state, player_id

    def get_state(self, player_id):
        """ Return player's state

        Args:
            player_id (int): player id

        Returns:
            (dict): The state of the player
        """
        state = self.dog_round.get_state(self.players, player_id)
        return state

    def get_legal_actions(self):
        """ Return the legal actions for current player

        Returns:
            (list): A list of legal actions
        """

        return self.dog_round.get_legal_actions()

    @staticmethod
    def get_action_num():
        """ Return the number of applicable actions

        Returns:
            (int): The number of actions. There are 78 actions
        """
        return 78

    def get_player_id(self):
        """ Return the current player's id

        Returns:
            (int): current player's id
        """
        return self.current_player_id

    def is_over(self):
        """ Check if the game is over

        Returns:
            (boolean): True if the game is over
        """
        return self.dog_round.is_over
