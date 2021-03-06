""" TAROT - CARD GAME - rule models
"""

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
            that appears least in the hand from legal actions.

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
        """ Step for evaluation. The same to step
        """
        return self.step(state)


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
