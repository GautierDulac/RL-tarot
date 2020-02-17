""" Wrrapers of pretrained models. Designed for Tensorflow.
"""

import os
from typing import List, Union

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
memory_init_size = 5000
norm_step = 1000


class TarotDQNModelV1(Model):
    """ A pretrained model on Tarot with DQN
    """

    def __init__(self, graph, sess):
        """ Load pretrained model
        """
        super().__init__()
        self.graph = graph
        self.sess = sess

        env = rlcard.make('tarot')
        with self.graph.as_default():
            self.dqn_agent = DQNAgent(self.sess,
                                      scope='dqn',
                                      action_num=78,  # env.action_num,
                                      replay_memory_size=20000,
                                      replay_memory_init_size=memory_init_size,
                                      norm_step=norm_step,
                                      state_shape=env.state_shape,
                                      mlp_layers=[512, 512])
            normalize(env, self.dqn_agent, 1000)
            self.sess.run(tf.compat.v1.global_variables_initializer())

        check_point_path = os.path.join(ROOT_PATH, 'tarot_v1')
        with self.sess.as_default():
            with self.graph.as_default():
                saver = tf.compat.v1.train.Saver(tf.compat.v1.model_variables())
                saver.restore(self.sess, tf.train.latest_checkpoint(check_point_path))

    @property
    def agents(self) -> Union[DQNAgent, List[DQNAgent]]:
        """
         Get a list of agents for each position in a the game
        :return: agents (list): A list of agents or an agent
        Note: Each agent should be just like RL agent with step and eval_step
              functioning well.
        """
        return self.dqn_agent

    @property
    def use_raw(self) -> bool:
        """
        Indicate whether use raw state and action
        :return: (boolean): True if using raw state and action
        """
        return False


class TarotDQNModelV10018(Model):
    """ A pretrained model on Tarot with DQN
    """

    def __init__(self, graph, sess):
        """ Load pretrained model
        """
        super().__init__()
        self.graph = graph
        self.sess = sess

        env = rlcard.make('tarot')
        with self.graph.as_default():
            self.dqn_agent = DQNAgent(self.sess,
                                      scope='dqn',
                                      action_num=78,  # env.action_num,
                                      replay_memory_size=20000,
                                      replay_memory_init_size=memory_init_size,
                                      norm_step=norm_step,
                                      state_shape=env.state_shape,
                                      mlp_layers=[512, 512])
            normalize(env, self.dqn_agent, 1000)
            self.sess.run(tf.compat.v1.global_variables_initializer())

        check_point_path = os.path.join(ROOT_PATH, 'self_played_1/tarot_v10018')
        with self.sess.as_default():
            with self.graph.as_default():
                saver = tf.compat.v1.train.Saver(tf.compat.v1.model_variables())
                saver.restore(self.sess, tf.train.latest_checkpoint(check_point_path))

    @property
    def agents(self) -> Union[DQNAgent, List[DQNAgent]]:
        """
         Get a list of agents for each position in a the game
        :return: agents (list): A list of agents or an agent
        Note: Each agent should be just like RL agent with step and eval_step
              functioning well.
        """
        return self.dqn_agent

    @property
    def use_raw(self) -> bool:
        """
        Indicate whether use raw state and action
        :return: (boolean): True if using raw state and action
        """
        return False


class TarotDQNModelV60073(Model):
    """ A pretrained model on Tarot with DQN
    """

    def __init__(self, graph, sess):
        """ Load pretrained model
        """
        super().__init__()
        self.graph = graph
        self.sess = sess

        env = rlcard.make('tarot')
        with self.graph.as_default():
            self.dqn_agent = DQNAgent(self.sess,
                                      scope='dqn',
                                      action_num=78,  # env.action_num,
                                      replay_memory_size=20000,
                                      replay_memory_init_size=memory_init_size,
                                      norm_step=norm_step,
                                      state_shape=env.state_shape,
                                      mlp_layers=[512, 1024, 512])
            normalize(env, self.dqn_agent, 1000)
            self.sess.run(tf.compat.v1.global_variables_initializer())

        check_point_path = os.path.join(ROOT_PATH, 'self_played_1/tarot_v60073')
        with self.sess.as_default():
            with self.graph.as_default():
                saver = tf.compat.v1.train.Saver(tf.compat.v1.model_variables())
                saver.restore(self.sess, tf.train.latest_checkpoint(check_point_path))

    @property
    def agents(self) -> Union[DQNAgent, List[DQNAgent]]:
        """
         Get a list of agents for each position in a the game
        :return: agents (list): A list of agents or an agent
        Note: Each agent should be just like RL agent with step and eval_step
              functioning well.
        """
        return self.dqn_agent

    @property
    def use_raw(self) -> bool:
        """
        Indicate whether use raw state and action
        :return: (boolean): True if using raw state and action
        """
        return False


class TarotDQNModelV110017(Model):
    """ A pretrained model on Tarot with DQN
    """

    def __init__(self, graph, sess):
        """ Load pretrained model
        """
        super().__init__()
        self.graph = graph
        self.sess = sess

        env = rlcard.make('tarot')
        with self.graph.as_default():
            self.dqn_agent = DQNAgent(self.sess,
                                      scope='dqn',
                                      action_num=78,  # env.action_num,
                                      replay_memory_size=20000,
                                      replay_memory_init_size=memory_init_size,
                                      norm_step=norm_step,
                                      state_shape=env.state_shape,
                                      mlp_layers=[512, 1024, 512])
            normalize(env, self.dqn_agent, 1000)
            self.sess.run(tf.compat.v1.global_variables_initializer())

        check_point_path = os.path.join(ROOT_PATH, 'self_played_11/tarot_v110017')
        with self.sess.as_default():
            with self.graph.as_default():
                saver = tf.compat.v1.train.Saver(tf.compat.v1.model_variables())
                saver.restore(self.sess, tf.train.latest_checkpoint(check_point_path))

    @property
    def agents(self) -> Union[DQNAgent, List[DQNAgent]]:
        """
         Get a list of agents for each position in a the game
        :return: agents (list): A list of agents or an agent
        Note: Each agent should be just like RL agent with step and eval_step
              functioning well.
        """
        return self.dqn_agent

    @property
    def use_raw(self) -> bool:
        """
        Indicate whether use raw state and action
        :return: (boolean): True if using raw state and action
        """
        return False


class TarotDQNModelV100(Model):
    """ A pretrained model on Tarot with DQN
    """

    def __init__(self, graph, sess):
        """ Load pretrained model
        """
        super().__init__()
        self.graph = graph
        self.sess = sess

        env = rlcard.make('tarot')
        with self.graph.as_default():
            self.dqn_agent = DQNAgent(self.sess,
                                      scope='dqn',
                                      action_num=78,  # env.action_num,
                                      replay_memory_size=20000,
                                      replay_memory_init_size=memory_init_size,
                                      norm_step=norm_step,
                                      state_shape=env.state_shape,
                                      mlp_layers=[512, 512])
            normalize(env, self.dqn_agent, 1000)
            self.sess.run(tf.compat.v1.global_variables_initializer())

        check_point_path = os.path.join(ROOT_PATH, 'tarot_v100')
        with self.sess.as_default():
            with self.graph.as_default():
                saver = tf.compat.v1.train.Saver(tf.compat.v1.model_variables())
                saver.restore(self.sess, tf.train.latest_checkpoint(check_point_path))

    @property
    def agents(self) -> Union[DQNAgent, List[DQNAgent]]:
        """
         Get a list of agents for each position in a the game
        :return: agents (list): A list of agents or an agent
        Note: Each agent should be just like RL agent with step and eval_step
              functioning well.
        """
        return self.dqn_agent

    @property
    def use_raw(self) -> bool:
        """
        Indicate whether use raw state and action
        :return: (boolean): True if using raw state and action
        """
        return False


def normalize(e: Env, agents: Union[DQNAgent, List[DQNAgent]], num: int) -> None:
    """
    Feed random data to normalizer
    :param e: AN Env class
    :param agents: A list of Agent object or an Agent object
    :param num: The number of steps to be normalized
    :return:
    """
    if isinstance(agents, DQNAgent):
        agents = [agents]
    begin_step = e.timestep
    e.set_agents([RandomAgent(e.action_num) for _ in range(e.player_num)])
    while e.timestep - begin_step < num:
        trajectories, _ = e.run(is_training=False)
        for agent in agents:
            for tra in trajectories:
                for ts in tra:
                    agent.feed(ts)
