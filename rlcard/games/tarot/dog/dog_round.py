from rlcard.games.tarot.alpha_and_omega.card import TarotCard
from rlcard.games.tarot.alpha_and_omega.player import TarotPlayer
from rlcard.games.tarot.bid.bid import TarotBid
from rlcard.games.tarot.dog.dog import TarotDog
from rlcard.games.tarot.utils import cards2list
from typing import List


class DogRound(object):

    def __init__(self, taking_player: TarotPlayer, taking_player_id: int, dog: TarotDog, num_cards_dog: int,
                 taking_bid: TarotBid):
        """ Initialize the round class

        Args:
            taking_player (int): the taking player that does the dog
        """
        self.num_cards_dog = num_cards_dog
        self.taking_player = taking_player
        self.taking_player_id = taking_player_id
        self.all_cards = taking_player.hand + dog
        self.taking_bid = taking_bid
        self.dog = dog
        self.new_dog = []
        self.is_over = False

    def proceed_round(self, players: List[TarotPlayer], played_card: TarotCard):
        """ Call other Classes's functions to keep one round running

        Args:
            :param played_card: string of legal action
            :param players: list of object of TarotPlayer
        """
        # remove corresponding card
        remove_index = None
        for index, card in enumerate(self.all_cards):
            if played_card.get_str() == card.get_str():
                remove_index = index
                break

        self.new_dog.append(self.all_cards.pop(remove_index))

        # When dog_cards cards in the dogs
        if len(self.new_dog) == self.num_cards_dog:
            players[self.taking_player_id].hand = self.all_cards
            self.is_over = True

        return self.taking_player_id

    def get_legal_actions(self):
        """
        Get all legal cards that can be put in the dog
        :return: list of legals TarotCard
        """
        legal_actions = []
        hand = self.all_cards
        # If without using king / trump, legal_actions >=3
        for card in hand:
            if not card.is_trump and card.color_value != 14:
                legal_actions.append(card)
        if len(legal_actions) == 0:
            for card in hand:
                if card.is_trump and card.trump_value not in [0, 1, 21]:
                    legal_actions.append(card)

        return legal_actions

    def get_state(self, players: List[TarotPlayer], player_id: int):
        """ Get player's state

        Args:
            players (list): The list of TarotPlayer
            player_id (int): The id of the player
        """
        state = {}
        # When dog is known
        others_hand = []
        for player in players:
            if player.player_id != player_id:
                others_hand.extend(player.hand)
        state['hand'] = cards2list(self.taking_player.hand)
        if self.taking_bid.get_bid_order() < 4:
            state['dog_cards'] = cards2list(self.new_dog)
        else:
            others_hand.extend(self.dog.hand)
            state['dog_cards'] = None
        state['others_hand'] = cards2list(others_hand)
        state['legal_actions'] = self.get_legal_actions()
        return state
