import unittest
import numpy as np

from rlcard.envs.tarot import TarotEnv as Env
from rlcard.agents.random_agent import RandomAgent
from rlcard.games.tarot.utils import ACTION_LIST


class TestTarotEnv(unittest.TestCase):

    def test_init_game_and_extract_state(self):
        env = Env()
        state, _ = env.init_game()
        self.assertEqual(state['obs'].size, 4 * 5 * 22)

    def test_get_legal_actions(self):
        env = Env()
        env.set_agents([RandomAgent(env.game.get_action_num()), RandomAgent(env.game.get_action_num())])
        env.init_game()
        legal_actions = env.get_legal_actions()
        for legal_action in legal_actions:
            self.assertLessEqual(legal_action, env.game.get_action_num())

    def test_step(self):
        env = Env()
        state, _ = env.init_game()
        action = np.random.choice(state['legal_actions'])
        _, player_id = env.step(action)
        self.assertEqual(player_id, env.game.round.current_player_id)

    def test_run(self):
        env = Env()
        env.set_agents([RandomAgent(env.game.get_action_num())] * env.game.get_player_num())
        trajectories, payoffs = env.run(is_training=False)
        self.assertEqual(len(trajectories), env.game.get_player_num())
        total = 0
        for payoff in payoffs:
            total += payoff
        self.assertEqual(total, 0)
        trajectories, payoffs = env.run(is_training=True, seed=1)
        total = 0
        for payoff in payoffs:
            total += payoff
        self.assertEqual(total, 0)

    def test_decode_action(self):
        env = Env()
        env.init_game()
        legal_actions = env.get_legal_actions()
        for legal_action in legal_actions:
            decoded = env.decode_action(legal_action)
            self.assertLessEqual(decoded.get_str(), ACTION_LIST[legal_action])

    def test_single_agent_mode(self):
        env = Env()
        env.set_mode(single_agent_mode=True)
        state = env.reset()
        self.assertIsInstance(state, dict)
        for _ in range(100):
            state, _, _ = env.step(np.random.choice(state['legal_actions']))

    def test_human_mode(self):
        env = Env()
        env.set_mode(human_mode=True)
        state = env.reset()
        self.assertIsInstance(state, dict)
        for _ in range(100):
            state, _, _ = env.step(np.random.choice(state['legal_actions']))


if __name__ == '__main__':
    unittest.main()
