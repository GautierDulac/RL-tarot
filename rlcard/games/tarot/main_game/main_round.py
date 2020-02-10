from typing import List

from rlcard.games.tarot.alpha_and_omega.card import TarotCard
from rlcard.games.tarot.alpha_and_omega.judger import TarotJudger
from rlcard.games.tarot.alpha_and_omega.player import TarotPlayer
from rlcard.games.tarot.utils import cards2list, get_end_pot_information


class MainRound(object):

    def __init__(self, starting_player_id: int, num_players: int, num_card_per_player: int, taking_bid_order: int,
                 new_dog: List[TarotCard]):
        """
        Initialize the round class
        :param starting_player_id: (int) id of the starting player
        :param num_players: (int)
        :param num_card_per_player: (int)
        :param taking_bid_order: (int) from 0 to 5
        :param new_dog: (List[TarotCard]) from dog part of the game
        """
        self.target_card = None
        self.highest_trump = -1
        self.current_player_id = starting_player_id
        self.num_players = num_players
        self.num_card_per_player = num_card_per_player
        self.direction = 1
        self.taking_bid_order = taking_bid_order
        self.played_cards = []
        self.pot_cards = dict()
        self.excuse_played = False
        self.excuse_player = None
        self.new_dog = new_dog
        self.is_pot_over = False
        self.is_over = False
        self.winner = None

    def proceed_round(self, players: List[TarotPlayer], played_card: TarotCard) -> int:
        """
        Call other Classes's functions to keep one round running
        :param players: (List[TarotPlayer]) list of the players
        :param played_card: (TarotCard) card chosen to be played
        :return:
        """
        player = players[self.current_player_id]

        if played_card.get_str() == 'TRUMP-0':
            self.excuse_played = True
            self.excuse_player = self.current_player_id

        # remove corresponding card
        remove_index = None
        for index, card in enumerate(player.hand):
            if played_card.get_str() == card.get_str():
                remove_index = index
                break

        _ = player.hand.pop(remove_index)

        # When starting a new pot
        if self.target_card is None and played_card.get_str() != 'TRUMP-0':
            self.highest_trump = -1
            self.target_card = played_card
            self.pot_cards['target'] = played_card

        # Add in Played_card list
        self.played_cards.append(played_card)

        # Add in pot_card
        self.pot_cards[self.current_player_id] = played_card

        # Keeping the highest trump of the pot
        if played_card.is_trump:
            self.highest_trump = max(self.highest_trump, int(played_card.trump_value))

        # When pot is over
        if len(self.played_cards) % self.num_players == 0:
            winner_id, pot_value, nb_bout = get_end_pot_information(self.pot_cards)
            if self.excuse_played:
                players[winner_id].points += pot_value - 4
                players[winner_id].bouts += nb_bout - 1
                players[self.excuse_player].points += 4
                players[self.excuse_player].bouts += 1
                # Erasing info about excuse
                self.excuse_player = None
                self.excuse_played = False
            else:
                players[winner_id].points += pot_value
                players[winner_id].bouts += nb_bout

            # Erasing target_card
            self.target_card = None

            # Printing values for debugging purpose # TODO REMOVE for training
            # print('================= Winner - '+str(int(len(self.played_cards)/4))+' =================')
            # print('\r>> Agent {} '.format(winner_id))
            # print('\r>> winning {} points'.format(pot_value))
            # print('')

            # Set game is over if no more card in hands
            if len(self.played_cards) == self.num_players * self.num_card_per_player:
                self.is_over = True
                self.winner = TarotJudger.judge_winner(players, self.new_dog)
            return winner_id

        return (self.current_player_id + 1) % self.num_players

    def get_legal_actions(self, players: List[TarotPlayer], player_id: int) -> List[TarotCard]:
        """
        Get all legal cards that can be played by current player with his hand and the target card
        :param players: list of all players
        :param player_id: current player
        :return: list of legals TarotCard
        """
        legal_actions = []
        hand = players[player_id].hand
        target = self.target_card
        # If no target card (first player to speak)
        if target is None:
            return hand
        # If there is a target
        else:
            target_color_is_trump = target.is_trump
            target_color = target.color
            # If color is not trump
            if not target_color_is_trump:
                for card in hand:
                    if card.color == target_color:
                        legal_actions.append(card)
                if len(legal_actions) == 0:
                    for card in hand:
                        if card.is_trump and card.trump_value > self.highest_trump:
                            legal_actions.append(card)
                if len(legal_actions) == 0:
                    for card in hand:
                        if card.is_trump:
                            legal_actions.append(card)
                if len(legal_actions) == 0:
                    legal_actions = hand
            # If asked is trump
            else:
                for card in hand:
                    if card.is_trump and card.trump_value > self.highest_trump:
                        legal_actions.append(card)
                if len(legal_actions) == 0:
                    for card in hand:
                        if card.is_trump:
                            legal_actions.append(card)
                if len(legal_actions) == 0:
                    legal_actions = hand

        return legal_actions

    def get_state(self, players: List[TarotPlayer], player_id: int) -> dict:
        """
        Get player's state
        :param players: The list of TarotPlayer
        :param player_id: The id of the player
        :return: (dict) containing:

                (List[str]) - hand: list of str tarotcards in hand
                (List[str]) - played_cards: list of all str-tarotcards played up to this moment
                (int) - pot_number
                (List[TarotCard]) - legal_actions: list of TarotCards available to be played
                (List[str]) - pot_cards: last few cards (str) played in the pot
                (str) - target: str-tarotcard of the target card in this pot (potentially None)
                (List[str]) - others_hand: list of str-tarotcards unknown
        """
        player = players[player_id]
        number_of_played_cards = len(self.played_cards)
        state = {'hand': cards2list(player.hand), 'played_cards': cards2list(self.played_cards),
                 'pot_number': int(number_of_played_cards / 4),
                 'legal_actions': self.get_legal_actions(players, player_id)}
        state['pot_cards'] = state['played_cards'][state['pot_number'] * 4:]
        if self.target_card is not None:
            state['target'] = self.target_card.get_str()
        else:
            state['target'] = None
        others_hand = []
        for player in players:
            if player.player_id != player_id:
                others_hand.extend(player.hand)
        # Dog is also in the others_hand group
        if self.taking_bid_order >= 4:
            others_hand.extend(self.new_dog)
        state['others_hand'] = cards2list(others_hand)
        return state
