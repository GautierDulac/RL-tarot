import numpy as np

from rlcard.envs.env import Env
from rlcard import models
from rlcard.games.tarot.main_game.main_game import TarotGame as Game
from rlcard.games.tarot.utils import encode_hand, encode_target, get_TarotCard_from_str
from rlcard.games.tarot.utils import ACTION_SPACE, ACTION_LIST
from rlcard.games.tarot.alpha_and_omega.card import TarotCard


class TarotEnv(Env):

    def __init__(self):
        super().__init__(Game())
        self.state_shape = [3, 5, 22]

    def print_state(self, player):
        """ Print out the state of a given player

        Args:
            player (int): Player id
        """
        # TODO : Adapt print depending on the part of the game, define a state['game_part'] ?
        state = self.game.get_state(player)

        print('================= Your Hand    ===============')
        TarotCard.print_cards(state['hand'])
        print('')
        print('================= Pot Number   ===============')
        print(state['pot_number'])
        print('')
        print('================= Target Card  ===============')
        TarotCard.print_cards(state['target'])
        print('')
        print('================= Pot Cards    ===============')
        TarotCard.print_cards(state['pot_cards'])
        print('')
        print('========== Actions You Can Choose ============')
        for i, action in enumerate(state['legal_actions']):
            print(str(ACTION_SPACE[action.get_str()]) + ': ', end='')
            TarotCard.print_cards(action.get_str())
            if i < len(state['legal_actions']) - 1:
                print(', ', end='')
        print('\n')

    def print_result(self, player):
        # TODO : Print results for the bid time
        # TODO : Adapt with the rank of players
        """ Print the game result when the game is over

        Args:
            player (int): The human player id
        """
        payoffs = self.get_payoffs()
        print('===============     Result     ===============')
        if payoffs[player] > 0:
            print('You win!')
        else:
            print('You lose!')
        print('')

    def print_action(self, action):
        # TODO : print depending on the game part
        """ Print out an action in a nice form

        Args:
            action (str): A string a action
        """
        TarotCard.print_cards(action)

    def load_model(self):
        # TODO : load model depending on the game part
        """ Load pretrained/rule model

        Returns:
            model (Model): A Model object
        """
        return models.load('tarot-rule-v1')

    def extract_state(self, state):
        # TODO : extract_state depending on the game part
        """

        :param state:
        :return:
        """
        obs = np.zeros((4, 5, 22), dtype=int)
        encode_hand(obs, state['hand'], index_to_encode=0)
        encode_target(obs[1], state['target'])
        encode_hand(obs, state['others_hand'], index_to_encode=2)
        encode_hand(obs, state['pot_cards'], index_to_encode=3)
        legal_action_id = self.get_legal_actions()
        extrated_state = {'obs': obs, 'legal_actions': legal_action_id}
        return extrated_state

    def get_payoffs(self):
        """
        Give final payoffs of the game
        :return:
        """
        return self.game.get_payoffs()

    def decode_action(self, action_id):
        # TODO : decode depending on the game part
        """

        :param action_id:
        :return: TarotCard - chosen action id or a random action in the avaiable ones
        :return: OR TarotBid ?
        """
        legal_ids = self.get_legal_actions()
        if action_id in legal_ids:
            return get_TarotCard_from_str(ACTION_LIST[action_id])
        return get_TarotCard_from_str(ACTION_LIST[np.random.choice(legal_ids)])

    def get_legal_actions(self):
        # TODO : depending on the game part
        """
        transform legal actions from game to the action_space legal actions
        :return:
        """
        legal_actions = self.game.get_legal_actions()
        legal_ids = [ACTION_SPACE[action.get_str()] for action in legal_actions]
        return legal_ids
