from typing import List, Union

import numpy as np

from rlcard import models
from rlcard.envs.env import Env
from rlcard.games.tarot.alpha_and_omega.card import TarotCard
from rlcard.games.tarot.bid.bid import TarotBid
from rlcard.games.tarot.global_game import GlobalGame as Game
from rlcard.games.tarot.utils import ACTION_SPACE, ACTION_LIST, BID_SPACE, BID_LIST
from rlcard.games.tarot.utils import encode_hand, encode_target, encode_bid, get_TarotCard_from_str, \
    get_TarotBid_from_str


class TarotEnv(Env):

    def __init__(self):
        # defining a self.game instance of GlobalGame
        super().__init__(Game())
        self.state_shape = [6, 5, 22]

    def print_state(self, player_id: int) -> None:
        """
        Print current state for a given player_id
        :param player_id:
        :return: No return
        """
        state = self.game.get_state(player_id)
        if self.game.current_game_part == 'BID':
            print('================= Your Hand    ===============')
            TarotCard.print_cards(state['hand'])
            print('')
            print('============== Current max Bid ===============')
            print(self.game.bid_game.bid_round.all_bids[state['max_bid']].get_str())
            print('')
            print('============ Current Personnal Bid ===========')
            if state['current_personal_bid'] is None:
                print('No bid yet')
            else:
                print(state['current_personal_bid'].get_str())
            print('')
            print('========== Actions You Can Choose ============')
            for i, bid in enumerate(state['legal_actions']):
                print(str(BID_SPACE[bid.get_str()]) + ': ', end='')
                print(bid.get_str() + ', ', end='')
                if i < len(state['legal_actions']) - 1:
                    print(' ', end='')
                else:
                    print('\n')
        elif self.game.current_game_part == 'DOG':
            print('================= Taking Bid =================')
            print(self.game.bid_game.bid_round.all_bids[state['taking_bid_order']].get_str())
            print('')
            if state['taking_bid_order'] < 4:
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
                    else:
                        print('\n')
            else:
                # No dog to be done
                print('================= Your Hand  =================')
                TarotCard.print_cards(state['hand'])
                print('')
                print('NO ACTION TO BE DONE')
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
                else:
                    print('\n')

    def print_result(self) -> None:
        """
        Print the game result when the game is over, not depending on any player_id
        :return: No return
        """
        payoffs = self.get_payoffs()
        print('===============     Result     ===============')
        print('Taking player: ' + str(self.game.taking_player_id) + ', with a ' +
              self.game.bid_game.bid_round.all_bids[self.game.taking_bid_order].get_str())
        print('This player did ' + str(self.game.players[self.game.taking_player_id].points) +
              ' with ' + str(self.game.players[self.game.taking_player_id].bouts) + ' bout(s)')
        print('Final winner(s) is/are: ' + str(self.game.main_game.main_round.winner))
        print('===============     Earned points     ===============')
        for key, value in payoffs.items():
            if value > 0:
                print('Player ' + str(key) + ' wins ' + str(value) + ' points !')
            else:
                print('Player ' + str(key) + ' loses ' + str(- value) + ' points !')
        print('')

    def print_action(self, action: Union[List[str], str]) -> None:
        """
        Print out an action in a nice form
        :param action: Must be a list of TarotCard strings (ex: 'SPADE-9') or a BID string ('PASSE')
        :return: No return, only print
        """
        if self.game.current_game_part == 'BID':
            print(action)
        else:
            TarotCard.print_cards(action)

    def load_model(self) -> dict:
        """
        Load pretrained/rule model
        :return: a dictionary with three models corresponding to each game part
        """
        return {'BID': models.load('tarot-bid-rule-v1'),
                'DOG': models.load('tarot-dog-rule-v1'),
                'MAIN': models.load('tarot-rule-v1')}

    def extract_state(self, state: dict) -> dict:
        """
        From the different possible state description (depending on the game part), return a dictionary with
        obs as a ndarray and legal_actions as a list of ids
        :param state: a dictionary with given information regarding the current game part
        :return: a dictionary with two information: obs (a ndarray) and legal_actions (a list)
        """
        obs = np.zeros((6, 5, 22), dtype=int)
        legal_action_id = self.get_legal_actions()
        extracted_state = {'legal_actions': legal_action_id}
        if self.game.current_game_part == 'BID':
            obs[0][0][0] = 0
            encode_hand(obs, state['hand'], index_to_encode=1)
            encode_bid(obs, state['current_personal_bid'], index_to_encode='2-0')
            encode_bid(obs, state['other_bids'], index_to_encode='2-1')
            extracted_state['obs'] = obs
        elif self.game.current_game_part == 'DOG':
            obs[0][0][0] = 1
            encode_hand(obs, state['all_cards'], index_to_encode=1)
            encode_bid(obs, state['taking_bid_order'], index_to_encode='2-0')
            encode_hand(obs, state['new_dog'], index_to_encode=3)
            encode_hand(obs, state['others_hand'], index_to_encode=4)
            extracted_state['obs'] = obs
        elif self.game.current_game_part == 'MAIN':
            obs[0][0][0] = 2
            encode_hand(obs, state['hand'], index_to_encode=1)
            encode_target(obs, state['target'], index_to_encode=2)
            encode_hand(obs, state['pot_cards'], index_to_encode=3)
            encode_hand(obs, state['played_cards'], index_to_encode=4)
            encode_hand(obs, state['others_hand'], index_to_encode=5)
            extracted_state['obs'] = obs
        else:
            raise ValueError
        return extracted_state

    def get_payoffs(self) -> dict:
        """
        Give final payoffs of the game
        :return: dictionary with player_id - won points
        """
        return self.game.get_payoffs()

    def decode_action(self, action_id: int) -> Union[TarotCard, TarotBid]:
        """
        Transform the selected action id into the relevant TarotBid or TarotCard object depending on the game part
        :param action_id: chosen ID from the model
        :return: TarotCard OR TarotBid - chosen action id or a random action in the avaiable ones
        :return:
        """
        legal_ids = self.get_legal_actions()
        if self.game.current_game_part == 'BID':
            if action_id in legal_ids:
                return get_TarotBid_from_str(BID_LIST[action_id])
            else:
                return get_TarotBid_from_str(BID_LIST[np.random.choice(legal_ids)])
        elif self.game.current_game_part in ['DOG', 'MAIN']:
            if action_id in legal_ids:
                return get_TarotCard_from_str(ACTION_LIST[action_id])
            else:
                return get_TarotCard_from_str(ACTION_LIST[np.random.choice(legal_ids)])
        else:
            raise ValueError

    def get_legal_actions(self) -> List[int]:
        """
        transform legal actions from game to the action_space legal actions
        :return: legal_ids, a list of int with all legal_ids for action for agents
        """
        legal_actions = self.game.get_legal_actions()
        if self.game.current_game_part == 'BID':
            legal_ids = [BID_SPACE[bid.get_str()] for bid in legal_actions]
            # TODO REMOVE IF UNRELEVANT - Adding a bias in the bid selection
            number_of_legal_actions = len(legal_ids)
            biased_legal_ids = []
            for index, bid_id in enumerate(legal_ids):
                biased_legal_ids = biased_legal_ids + [bid_id] * 2 ** (number_of_legal_actions - index - 1)
            return legal_ids
        elif self.game.current_game_part in ['DOG', 'MAIN']:
            legal_ids = [ACTION_SPACE[action.get_str()] for action in legal_actions]
            return legal_ids
        else:
            raise ValueError
