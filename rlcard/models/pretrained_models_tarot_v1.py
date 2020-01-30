""" Wrrapers of pretrained models. Designed for Tensorflow.
"""

import os
from typing import List

import tensorflow as tf

import rlcard
from rlcard.agents.dqn_agent import DQNAgent
from rlcard.agents.random_agent import RandomAgent
from rlcard.envs.env import Env
from rlcard.models.model import Model

# Root path of pretrianed models
ROOT_PATH = os.path.join(rlcard.__path__[0], 'models/pretrained')

# Set the the number of steps for collecting normalization statistics
# and intial memory size
memory_init_size = 1000
norm_step = 100


class TarotDQNModelV1(Model):
    """ A pretrained model on Tarot with DQN
    """

    def __init__(self):
        """ Load pretrained model
        """
        super().__init__()
        self.graph = tf.Graph()
        self.sess = tf.Session(graph=self.graph)

        env = rlcard.make('tarot')
        with self.graph.as_default():
            self.dqn_agents = []
            for i in range(env.player_num):
                agent = DQNAgent(self.sess,
                                 scope='dqn',
                                 action_num=78,  # env.action_num,
                                 replay_memory_size=20000,
                                 replay_memory_init_size=memory_init_size,
                                 norm_step=norm_step,
                                 state_shape=env.state_shape,
                                 mlp_layers=[512, 512])
                self.dqn_agents.append(agent)
            normalize(env, self.dqn_agents, 1000)
            self.sess.run(tf.global_variables_initializer())

        check_point_path = os.path.join(ROOT_PATH, 'tarot_v1')
        with self.sess.as_default():
            with self.graph.as_default():
                saver = tf.train.Saver(tf.model_variables())
                saver.restore(self.sess, tf.train.latest_checkpoint(check_point_path))

    @property
    def agents(self) -> List[DQNAgent]:
        """
         Get a list of agents for each position in a the game
        :return: agents (list): A list of agents
        Note: Each agent should be just like RL agent with step and eval_step
              functioning well.
        """
        return self.dqn_agents

    @property
    def use_raw(self) -> bool:
        """
        Indicate whether use raw state and action
        :return: (boolean): True if using raw state and action
        """
        return False


def normalize(e: Env, agents: List[DQNAgent], num: int) -> None:
    """
    Feed random data to normalizer
    :param e: AN Env class
    :param agents: A list of Agent object
    :param num: The number of steps to be normalized
    :return:
    """
    begin_step = e.timestep
    e.set_agents([RandomAgent(e.action_num) for _ in range(e.player_num)])
    while e.timestep - begin_step < num:
        trajectories, _ = e.run(is_training=False)
        for agent in agents:
            for tra in trajectories:
                for ts in tra:
                    agent.feed(ts)
