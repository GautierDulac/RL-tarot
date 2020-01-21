import numpy as np

from rlcard.games.tarot.card import TarotCard
from rlcard.games.tarot.utils import cards2list, WILD, WILD_DRAW_4


class TarotRound(object):

    def __init__(self, dealer, num_players):
        ''' Initialize the round class

        Args:
            dealer (object): the object of TarotDealer
            num_players (int): the number of players in game
        '''
        self.dealer = dealer
        self.target = None
        self.current_player = 0
        self.num_players = num_players
        self.direction = 1
        self.played_cards = []
        self.is_over = False
        self.winner = None

    def proceed_round(self, players, action):
        # TODO : adapt for TAROT
        ''' Call other Classes's functions to keep one round running

        Args:
            player (object): object of TarotPlayer
            action (str): string of legal action
        '''
        if action == 'draw':
            self._perform_draw_action(players)
            return None
        player = players[self.current_player]
        card_info = action.split('-')
        color = card_info[0]
        trait = card_info[1]
        # remove correspongding card
        remove_index = None
        if trait == 'wild' or trait == 'wild_draw_4':
            for index, card in enumerate(player.hand):
                if trait == card.trait:
                    remove_index = index
                    break
        else:
            for index, card in enumerate(player.hand):
                if color == card.color and trait == card.trait:
                    remove_index = index
                    break
        card = player.hand.pop(remove_index)
        if not player.hand:
            self.is_over = True
            self.winner = [self.current_player]
        self.played_cards.append(card)

        # perform the number action
        if card.type == 'number':
            self.current_player = (self.current_player + self.direction) % self.num_players
            self.target = card

        # perform non-number action
        else:
            self._preform_non_number_action(players, card)

    def get_legal_actions(self, players, player_id):
        # TODO : Adapt for TAROT
        wild_flag = 0
        wild_draw_4_flag = 0
        legal_actions = []
        wild_4_actions = []
        hand = players[player_id].hand
        target = self.target
        if target.type == 'wild':
            for card in hand:
                if card.type == 'wild':
                    # card.color = np.random.choice(TarotCard.info['color'])
                    if card.trait == 'wild_draw_4':
                        if wild_draw_4_flag == 0:
                            wild_draw_4_flag = 1
                            wild_4_actions.extend(WILD_DRAW_4)
                    else:
                        if wild_flag == 0:
                            wild_flag = 1
                            legal_actions.extend(WILD)
                elif card.color == target.color:
                    legal_actions.append(card.str)

        # target is action card or number card
        else:
            for card in hand:
                if card.type == 'wild':
                    if card.trait == 'wild_draw_4':
                        if wild_draw_4_flag == 0:
                            wild_draw_4_flag = 1
                            wild_4_actions.extend(WILD_DRAW_4)
                    else:
                        if wild_flag == 0:
                            wild_flag = 1
                            legal_actions.extend(WILD)
                elif card.color == target.color or card.trait == target.trait:
                    legal_actions.append(card.str)
        if not legal_actions:
            legal_actions = wild_4_actions
        if not legal_actions:
            legal_actions = ['draw']
        return legal_actions

    def get_state(self, players, player_id):
        # TODO : Adapt for TAROT
        ''' Get player's state

        Args:
            players (list): The list of TarotPlayer
            player_id (int): The id of the player
        '''
        state = {}
        player = players[player_id]
        state['hand'] = cards2list(player.hand)
        state['target'] = self.target.str
        state['played_cards'] = cards2list(self.played_cards)
        others_hand = []
        for player in players:
            if player.player_id != player_id:
                others_hand.extend(player.hand)
        state['others_hand'] = cards2list(others_hand)
        state['legal_actions'] = self.get_legal_actions(players, player_id)
        return state
