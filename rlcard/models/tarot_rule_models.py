''' TAROT rule models
'''

import numpy as np

import rlcard
from rlcard.models.model import Model


class TAROTRuleAgentV1(object):
    """ TAROT Rule agent version 1
    """

    def __init__(self):
        pass

    def step(self, state):
        """ Predict the action given raw state. A naive rule. Choose the color
            that appears least in the hand from legal actions. Try to keep wild
            cards as long as it can.

        Args:
            state (dict): Raw state from the game

        Returns:
            action (str): Predicted action
        """

        legal_actions = state['legal_actions']

        # We randomly choose one
        action = np.random.choice(legal_actions)
        return action

    def eval_step(self, state):
        ''' Step for evaluation. The same to step
        '''
        return self.step(state)

    @staticmethod
    def filter_wild(hand):
        ''' Filter the wild cards. If all are wild cards, we do not filter

        Args:
            hand (list): A list of TAROT card string

        Returns:
            filtered_hand (list): A filtered list of TAROT string
        '''
        filtered_hand = []
        for card in hand:
            if not card[2:6] == 'wild':
                filtered_hand.append(card)

        if len(filtered_hand) == 0:
            filtered_hand = hand

        return filtered_hand

    @staticmethod
    def count_colors(hand):
        ''' Count the number of cards in each color in hand

        Args:
            hand (list): A list of TAROT card string

        Returns:
            color_nums (dict): The number cards of each color
        '''
        color_nums = {}
        for card in hand:
            color = card[0]
            if color not in color_nums:
                color_nums[color] = 0
            color_nums[color] += 1

        return color_nums


class TAROTRuleModelV1(Model):
    """ TAROT Rule Model version 1
    """

    def __init__(self):
        """ Load pretrained model
        """
        super().__init__()
        env = rlcard.make('tarot')

        rule_agent = TAROTRuleAgentV1()
        self.rule_agents = [rule_agent for _ in range(env.player_num)]

    @property
    def agents(self):
        """ Get a list of agents for each position in a the game

        Returns:
            agents (list): A list of agents

        Note: Each agent should be just like RL agent with step and eval_step
              functioning well.
        """
        return self.rule_agents

    @property
    def use_raw(self):
        """ Indicate whether use raw state and action

        Returns:
            use_raw (boolean): True if using raw state and action
        """
        return True
