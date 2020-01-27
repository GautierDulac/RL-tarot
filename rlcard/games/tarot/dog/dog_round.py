from typing import List

from rlcard.games.tarot.alpha_and_omega.card import TarotCard
from rlcard.games.tarot.alpha_and_omega.player import TarotPlayer
from rlcard.games.tarot.dog.dog import TarotDog
from rlcard.games.tarot.utils import cards2list


class DogRound(object):

    def __init__(self, taking_player: TarotPlayer, taking_player_id: int, dog: TarotDog, num_cards_dog: int,
                 taking_bid_order: int):
        """
        Initialize the DogRound class
        :param taking_player: (TarotPlayer) player that won the bid contest
        :param taking_player_id: (int) id of that player
        :param dog: (TarotDog) dog initialized earlier
        :param num_cards_dog: (int)
        :param taking_bid_order: (in) from 0 to 5 representing the order of the winning bid
        """
        self.num_cards_dog = num_cards_dog
        self.taking_player = taking_player
        self.taking_player_id = taking_player_id
        self.taking_bid_order = taking_bid_order
        if self.taking_bid_order < 4:
            self.all_cards = taking_player.hand + dog.hand
            self.new_dog = []
        else:
            self.all_cards = taking_player.hand
            self.new_dog = dog.hand
        self.dog = dog
        self.is_over = False

    def proceed_round(self, players: List[TarotPlayer], played_card: TarotCard) -> int:
        """
        Call other Classes's functions to keep one round running
        :param played_card: (TarotCard) object with the chosen card to be played
        :param players: list of TarotPlayer object
        :return: (int) id of next player (mainly the same here)
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

    def get_legal_actions(self) -> List[TarotCard]:
        """
        Get all legal cards that can be put in the dog
        :return: list of legals TarotCard
        """
        if self.taking_bid_order >= 4:
            # No dog to be done
            raise ValueError
        legal_actions = []
        hand = self.all_cards
        # If without using king / trump, legal_actions > 0
        for card in hand:
            if not card.is_trump and card.color_value != 14:
                legal_actions.append(card)
        if len(legal_actions) == 0:
            for card in hand:
                if card.is_trump and card.trump_value not in [0, 1, 21]:
                    legal_actions.append(card)

        return legal_actions

    def get_state(self, players: List[TarotPlayer], player_id: int) -> dict:
        """
        Get the current state for the concerned player_id
        :param players: (List[TarotPlayer])
        :param player_id: (int)
        :return: (dict) containing:

                (int) - taking_bid_order: from 0 to 5, bid order
                (List[TarotCard]) - legal_actions: list of legal actions
                (List[str]) - hand: List of str cards in hand
                (List[str]) - all_cards: List of all known str cards (eather hand if bid is GARDE_SANS ou CONTRE, or also containing the dog cards in the other way round)
                (List[str]) - new_dog: List of the str cards in the new dog if he is known, None otherwise
                (List[str]) - others_hand: List of the str cards that are not known
        """
        state = {'taking_bid_order': self.taking_bid_order,
                 'legal_actions': self.get_legal_actions(), 'hand': cards2list(self.taking_player.hand)}
        # When dog is known
        others_hand = []
        for player in players:
            if player.player_id != player_id:
                others_hand.extend(player.hand)
        if self.taking_bid_order < 4:
            state['all_cards'] = cards2list(self.all_cards)
            state['new_dog'] = cards2list(self.new_dog)
        # otherwise
        else:
            state['all_cards'] = state['hand']
            state['new_dog'] = None
            others_hand.extend(self.dog.hand)
        state['others_hand'] = cards2list(others_hand)
        return state
