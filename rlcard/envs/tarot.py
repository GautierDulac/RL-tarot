import numpy as np

from rlcard.envs.env import Env
from rlcard import models
from rlcard.games.tarot.global_game import GlobalGame as Game
from rlcard.games.tarot.utils import encode_hand, encode_target, get_TarotCard_from_str
from rlcard.games.tarot.utils import ACTION_SPACE, ACTION_LIST, BID_SPACE, BID_LIST
from rlcard.games.tarot.alpha_and_omega.card import TarotCard


class TarotEnv(Env):

    def __init__(self):
        # defining a self.game instance of GlobalGame
        super().__init__(Game())

    def print_state(self, player):
        """ Print out the state of a given player

        Args:
            player (int): Player id
        """
        state = self.game.get_state(player)
        if self.game.current_game_part == 'BID':
            print('================= Your Hand    ===============')
            TarotCard.print_cards(state['hand'])
            print('')
            print('============== Current max Bid ===============')
            print(self.game.bid_game.bid_round.all_bids[state['max_bid']])
            print('')
            print('============ Current Personnal Bid ===========')
            print(state['current_personnal_bid'].get_str())
            print('')
            print('========== Actions You Can Choose ============')
            for i, bid in enumerate(state['legal_actions']):
                print(str(BID_SPACE[bid.get_str()]) + ': ', end='')
                print(bid.get_str() + ', ', end='')
                if i < len(state['legal_actions']) - 1:
                    print(' ', end='')
            print('\n')
            return
        elif self.game.current_game_part == 'DOG':
            print('================= Taking Bid =================')
            print(self.game.bid_game.bid_round.all_bids[state['taking_bid']])
            print('')
            if state['taking_bid'] < 4:
                # Dog has to be done
                print('================= Total Hand =================')
                TarotCard.print_cards(state['all_cards'])
                print('')
                print('============= Current New Dog ================')
                TarotCard.print_cards(state['new_dog'])
                print('')
                print('============ Cards You Can Choose ============')
                for i, action in enumerate(state['legal_actions']):
                    print(str(ACTION_SPACE[action.get_str()]) + ': ', end='')
                    TarotCard.print_cards(action.get_str())
                    if i < len(state['legal_actions']) - 1:
                        print(', ', end='')
                print('\n')
            else:
                # No dog to be done
                print('================= Your Hand  =================')
                TarotCard.print_cards(state['hand'])
                print('')
                print('NO ACTION TO BE DONE')
            return
        elif self.game.current_game_part == 'MAIN':
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
        # The Bid game is not printed
        """ Print the game result when the game is over

        Args:
            player (int): The human player id
        """
        payoffs = self.get_payoffs()
        print('===============     Result     ===============')
        payoffs = sorted(payoffs, key=payoffs.get)
        print('Taking player : ' + str(self.game.taking_player_id) + ', with a ' + self.game.taking_bid.get_str())
        print('This player did ' + str(self.game.players[self.game.taking_player_id].points) +
              ' with ' + str(self.game.players[self.game.taking_player_id].bouts))
        print('Final winner(s) is/are :' + str(self.game.main_game.main_round.winner))
        print('===============     Earned points     ===============')
        for key, value in enumerate(payoffs):
            if value > 0:
                print('Player ' + str(key) + ' wins ' + str(value) + ' points !')
            else:
                print('Player ' + str(key) + 'loses ' + str(- value) + 'points !')
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
