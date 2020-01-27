from typing import List

from rlcard.games.tarot.alpha_and_omega.card import TarotCard
from rlcard.games.tarot.alpha_and_omega.player import TarotPlayer
from rlcard.games.tarot.dog.dog import TarotDog
from rlcard.games.tarot.dog.dog_round import DogRound


class DogGame(object):

    def __init__(self, players: List[TarotPlayer], taking_player_id: int,
                 num_cards_per_player: int, num_cards_dog: int, dog: TarotDog, taking_bid_order: int):
        """
        Initialize a DogGame object
        :param players: (List[TarotPlayer]) list of TarotPlayer in the whole game
        :param taking_player_id: (int) Player_id that won the BID contest
        :param num_cards_per_player: (int) number of cards per player
        :param num_cards_dog: (int) number of cards in the dog
        :param dog: (TarotDog) dog object initialized in the begining
        :param taking_bid_order: (int) order of the taken bid (from 0 to 5)
        """
        self.num_cards_per_player = num_cards_per_player
        self.num_cards_dog = num_cards_dog
        # Initialize players
        self.players = players
        self.taking_player = players[taking_player_id]
        self.current_player_id = taking_player_id
        # Initialize the dog round
        self.dog_round = DogRound(self.taking_player, taking_player_id, dog, num_cards_dog, taking_bid_order)
        # Taking bid for the taking player
        self.taking_bid_order = taking_bid_order
        # Is over ?
        self.is_over = False

    def init_game(self) -> (dict, int):
        """
        Initialize Status for Dog Round
        :return: (tuple): containing :

                (dict): the current state
                (int): next player id
        """
        player_id = self.dog_round.taking_player_id
        state = self.get_state(player_id)

        return state, player_id

    def step(self, played_dog_card: TarotCard) -> (dict, int):
        """
        Get the next state
        :param played_dog_card: (TarotCard) the card chosen to be put in the dog
        :return: (tuple): Tuple containing:

                (dict): next player's state
                (int): next plater's id
        """
        player_id = self.dog_round.proceed_round(self.players, played_dog_card)

        if self.dog_round.is_over:
            self.is_over = True

        state = self.get_state(player_id)
        return state, player_id

    def get_state(self, player_id: int) -> dict:
        """
        Return player's state
        :param player_id: (int) player_id
        :return: (dict): The state of the player
        """
        state = self.dog_round.get_state(self.players, player_id)
        return state

    def get_legal_actions(self) -> List[TarotCard]:
        """
        Return the legal actions for current player
        :return: (List[TarotCard]) - List of legal cards to be put in the dog
        """
        return self.dog_round.get_legal_actions()

    @staticmethod
    def get_action_num() -> int:
        """
        Return the number of applicable actions
        :return: (int): The number of actions. There are 78 actions
        """
        return 78

    def get_player_id(self) -> int:
        """
        Return the current player's id
        :return: (int): current player's id
        """
        return self.current_player_id

    def is_over(self) -> bool:
        """
        Check if the game is over
        :return: (boolean): True if the game is over
        """
        return self.dog_round.is_over
