# Understand STATE management ?
# Add initial rules for first pot

from rlcard.games.tarot.card import TarotCard
from rlcard.games.tarot.player import TarotPlayer
from rlcard.games.tarot.utils import cards2list


class TarotRound(object):

    def __init__(self, dealer, num_players):
        """ Initialize the round class

        Args:
            dealer (object): the object of TarotDealer
            num_players (int): the number of players in game
        """
        self.dealer = dealer
        self.target_card = None
        self.highest_trump = 0
        self.current_player = 0
        self.num_players = num_players
        self.direction = 1
        self.played_cards = []
        self.is_pot_over = False
        self.is_over = False
        self.winner = None

    def proceed_round(self, players: list[TarotPlayer], played_card: TarotCard):
        """ Call other Classes's functions to keep one round running

        Args:
            :param played_card: string of legal action
            :param players: list of object of TarotPlayer
        """
        player = players[self.current_player]

        # remove corresponding card
        remove_index = None
        for index, card in enumerate(player.hand):
            if played_card == card:
                remove_index = index
                break

        _ = player.hand.pop(remove_index)

        if played_card.is_trump:
            self.highest_trump = max(self.highest_trump, played_card.trump_value)

    def get_legal_actions(self, players: list[TarotPlayer], player_id):
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
            return hand  # TODO : add rules for playing initial color
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

    def get_state(self, players, player_id):
        # TODO : Adapt state for TAROT?
        """ Get player's state

        Args:
            players (list): The list of TarotPlayer
            player_id (int): The id of the player
        """
        state = {}
        player = players[player_id]
        state['hand'] = cards2list(player.hand)
        state['target'] = self.target_card.str
        state['played_cards'] = cards2list(self.played_cards)
        others_hand = []
        for player in players:
            if player.player_id != player_id:
                others_hand.extend(player.hand)
        state['others_hand'] = cards2list(others_hand)
        state['legal_actions'] = self.get_legal_actions(players, player_id)
        return state
