import random
from typing import Union, List

import numpy as np

# TODO - WARNING - Some changes done compared to initial environment
from rlcard.agents.dqn_agent import DQNAgent
from rlcard.agents.random_agent import RandomAgent
from rlcard.games.tarot.alpha_and_omega.card import TarotCard
from rlcard.games.tarot.bid.bid import TarotBid
from rlcard.games.tarot.global_game import GlobalGame
from rlcard.utils.utils import reorganize


class Env(object):

    def __init__(self, game: GlobalGame, allow_step_back=False):
        """
        Initialize
        :param game: GlobalGame object
        :param allow_step_back: UNUSED
        """
        self.state_shape = None
        self.name = None
        self.game = game
        self.allow_step_back = allow_step_back
        self.agents = None

        # Get number of players/actions in this game
        self.player_num = game.get_player_num()
        self.action_num = 78  # game.get_action_num() TODO : Modify for 78 everytime (6 < 78)

        # A counter for the timesteps
        self.timestep = 0

        # MODES
        self.single_agent_mode = False
        self.active_player = None
        self.human_mode = False

        self.model = None

    def init_game(self) -> (np.ndarray, int):
        """
        Start a new game
        :return: (tuple): Tuple containing:

                (numpy.array): The begining state of the game
                (int): The begining player
        """
        state, player_id = self.game.init_game()
        return self.extract_state(state), player_id

    def step(self, action: int) -> (np.ndarray, int):
        """
        Step forward
        :param action: the action id taken by the current player
        :return: (tuple): Tuple containing:

                (numpy.array): The next state
                (int): The ID of the next player
        """
        if self.single_agent_mode or self.human_mode:
            print('\r>> Agent 0 (Human) chooses ', end='')
            self.print_action(self.decode_action(action).get_str())
            print('')
            return self.single_agent_step(action)

        self.timestep += 1
        next_state, player_id = self.game.step(self.decode_action(action))

        return self.extract_state(next_state), player_id

    def single_agent_step(self, action: int) -> (np.ndarray, int):
        """
        Step forward for human/single agent
        :param action: id of the chosen action
        :return: (tuple) containing:

                (np.ndarray): the next state
                (int): the reward
                (bool): a 'done' information # TODO understand done - REMOVED FOR NOW WARNING ?
        """
        reward = 0.
        self.timestep += 1
        state, player_id = self.game.step(self.decode_action(action))
        while not self.game.is_over() and not player_id == self.active_player:
            self.timestep += 1
            if self.model[self.game.current_game_part].use_raw:
                action = self.model[self.game.current_game_part].agents[player_id].eval_step(state)
            else:
                action = self.model[self.game.current_game_part].agents[player_id].eval_step(self.extract_state(state))
                action = self.decode_action(action)
            if self.human_mode:
                print('\r>> Agent {} chooses '.format(player_id), end='')
                self.print_action(action.get_str())
                print('')
            state, player_id = self.game.step(action)

        if self.game.is_over():
            reward = self.get_payoffs()[self.active_player]
            if self.human_mode:
                self.print_result()
            state = self.reset()
            return state, reward

        elif self.human_mode:
            self.print_state(self.active_player)

        return self.extract_state(state), reward

    def reset(self) -> dict:
        """
        Reset environment in single-agent mode
        :return: the extract_state dict with obs and legal_ids
        """
        if not self.single_agent_mode and not self.human_mode:
            raise ValueError('Reset can only be used in single-agent mode or human mode')
        history = []
        while True:
            print('\n>> Start a new game!')
            state, player_id = self.game.init_game()
            while not player_id == self.active_player:
                self.timestep += 1
                if self.model[self.game.current_game_part].use_raw:
                    action = self.model[self.game.current_game_part].agents[player_id].eval_step(state)
                else:
                    action = self.model[self.game.current_game_part].agents[player_id].eval_step(
                        self.extract_state(state))
                    action = self.decode_action(action)
                print('\r>> Agent {} chooses '.format(player_id), end='')
                self.print_action(action.str)
                print('')
                state, player_id = self.game.step(action)

            if not self.game.is_over():
                if self.human_mode:
                    self.print_state(self.active_player)
                break
            else:
                if self.human_mode:
                    history.clear()

        return self.extract_state(state)

    def step_back(self) -> (np.ndarray, int):
        """
        Take one step backward.
        :return: (tuple): Tuple containing:

                (numpy.array): The previous state
                (int): The ID of the previous player
        Note: Error will be raised if step back from the root node.
        """
        if not self.allow_step_back:
            raise Exception('Step back is off. To use step_back, please set allow_step_back=True in rlcard.make')

        if not self.game.step_back():
            return False

        player_id = self.get_player_id()
        state = self.get_state(player_id)

        return state, player_id

    def get_player_id(self) -> int:
        """
        Get the current player id
        :return: (int): the id of the current player
        """
        return self.game.get_player_id()

    def is_over(self) -> bool:
        """
        Check whether the curent game is over
        :return: (boolean): True is current game is over
        """
        return self.game.is_over()

    def get_state(self, player_id: int) -> dict:
        """
        Get the state given player id
        :param player_id: (int): The player id
        :return: (tuple) containing:

                (numpy.array): The observed state of the player
                (list): the ids of legal actions
        """
        return self.extract_state(self.game.get_state(player_id))

    def set_agents(self, agents: List[Union[RandomAgent, DQNAgent]]) -> None:
        """
        Set the agents that will interact with the environment
        :param agents: List of Agent classes
        :return:
        """
        if self.single_agent_mode or self.human_mode:
            raise ValueError('Setting agent in single agent mode or human mode is not allowed.')

        self.agents = agents

    def run(self, is_training: bool = False, seed: int = None) -> (List[List[dict]], dict):
        """
        Run a complete game, either for evaluation or training RL agent.
        :param is_training: (boolean): True if for training purpose.
        :param seed: (int): A seed for running the game. For single-process program,
              the seed should be set to None. For multi-process program, the
              seed should be asigned for reproducibility.
        :return: (tuple) Tuple containing:

                (list): A list of trajectories generated from the environment.
                (list): A list payoffs. Each entry corresponds to one player.

        Note: The trajectories are 3-dimension list. The first dimension is for different players.
              The second dimension is for different transitions. The third dimension is for the contents of each transiton
        """
        if self.single_agent_mode or self.human_mode:
            raise ValueError('Run in single agent mode or human mode is not allowed.')

        if seed is not None:
            np.random.seed(seed)
            random.seed(seed)

        trajectories = [[] for _ in range(self.player_num)]
        state, player_id = self.init_game()

        # Loop to play the game
        trajectories[player_id].append(state)

        while not self.is_over():

            # Agent plays
            if not is_training:
                action = self.agents[player_id].eval_step(state)
            else:
                action = self.agents[player_id].step(state)

            # Environment steps
            next_state, next_player_id = self.step(action)
            # Save action
            trajectories[player_id].append(action)

            # Set the state and player
            state = next_state
            player_id = next_player_id

            # Save state.
            if not self.game.is_over():
                trajectories[player_id].append(state)

        # Add a final state to all the players
        for player_id in range(self.player_num):
            state = self.get_state(player_id)
            trajectories[player_id].append(state)

        # Payoffs
        payoffs = self.get_payoffs()

        # Reorganize the trajectories
        trajectories = reorganize(trajectories, payoffs)

        return trajectories, payoffs

    def run_multi(self, task_num: int, result: List, is_training: bool = False, seed: int = None) -> None:
        """
        UNUSED function for now - must depend on the agents used ?
        :param task_num:
        :param result:
        :param is_training:
        :param seed:
        :return:
        """
        if seed is not None:
            np.random.seed(seed)
        for _ in range(task_num):
            result.append(self.run(is_training=is_training))

    def set_mode(self, active_player: int = 0, single_agent_mode: bool = False, human_mode: bool = False) -> None:
        """
        Turn on the single-agent-mode. Pretrained models will be loaded to simulate other agents
        :param active_player: The player that does not use pretrained models
        :param single_agent_mode:
        :param human_mode:
        :return: None
        """
        if not isinstance(active_player, int) or active_player < 0 or active_player >= self.player_num:
            raise ValueError('Active player should be a positiv integer less than the player number')

        if not single_agent_mode and not human_mode:
            raise ValueError('You must set single_agent_mode=True, or human_mode=True')

        if single_agent_mode and human_mode:
            raise ValueError('You can not set single_agentmode=True and human_mode=True together/')

        self.model = self.load_model()
        self.active_player = active_player
        self.single_agent_mode = single_agent_mode
        self.human_mode = human_mode

    def print_state(self, player: int) -> None:
        """
        Print out the state of a given player
        :param player: (int): Player id
        :return: Nothing
        """
        raise NotImplementedError

    def print_result(self) -> None:
        """
        Print the game result when the game is over
        :return: Nothing
        """
        raise NotImplementedError

    @staticmethod
    def print_action(action: Union[List[str], str]) -> None:
        """
        Print out an action in a nice form
        :param action: Must be a list of TarotCard strings (ex: 'SPADE-9') or a BID string ('PASSE')
        :return: No return, only print
        """
        raise NotImplementedError

    def load_model(self) -> dict:
        """
        Specific for Tarot, in other games, directly return one model
        Load pretrained/rule model
        :return: a dictionary with three models corresponding to each game part
        """
        raise NotImplementedError

    def extract_state(self, state: dict) -> dict:
        """
        From the different possible state description (depending on the game part), return a dictionary with
        obs as a ndarray and legal_actions as a list of ids
        :param state: a dictionary with given information regarding the current game part
        :return: a dictionary with two information: obs (a ndarray) and legal_actions (a list)
        """
        raise NotImplementedError

    def get_payoffs(self) -> dict:
        """
        Give final payoffs of the game
        :return: dictionary with player_id - won points
        """
        raise NotImplementedError

    def decode_action(self, action_id: int) -> Union[TarotBid, TarotCard]:
        """
        Transform the selected action id into the relevant TarotBid or TarotCard object depending on the game part
        :param action_id: chosen ID from the model
        :return: TarotCard OR TarotBid - chosen action id or a random action in the avaiable ones
        :return:
        """
        raise NotImplementedError

    def get_legal_actions(self) -> List[int]:
        """
        transform legal actions from game to the action_space legal actions
        :return: legal_ids, a list of int with all legal_ids for action for agents
        """
        raise NotImplementedError
