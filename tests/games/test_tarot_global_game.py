import unittest
import numpy as np
import random

from rlcard.games.tarot.global_game import GlobalGame
from rlcard.games.tarot.bid.bid import TarotBid
from rlcard.games.tarot.utils import ACTION_LIST


class TestTarotMainGameMethods(unittest.TestCase):
    def test_is_over(self):
        game = GlobalGame()
        game.init_game()
        self.assertIsInstance(game.is_over(), bool)

    def test_global_over(self):
        game = GlobalGame()
        game.init_game()
        while not game.is_over:
            action = np.random.choice(game.get_legal_actions())
            state, _ = game.step(action)
            self.assertEqual(game.is_over, game.bid_over and game.dog_over and game.main_over)
            self.assertLessEqual(len(game.players[0].hand), game.num_cards_per_player)
            self.assertLessEqual(len(state['hand']), game.num_cards_per_player)

    def test_global_game(self):
        game = GlobalGame()
        game.init_game()
        went_though_dog = 0
        went_though_main = 0
        iteration = 0
        while not game.is_over():
            print(game.current_game_part)
            iteration += 1
            action = np.random.choice(game.get_legal_actions())
            print(action.get_str())
            state, _ = game.step(action)
            if game.current_game_part == 'BID':
                self.assertIn(np.random.choice(game.get_legal_actions()).get_str(), TarotBid.order.keys())
            if game.current_game_part == 'DOG':
                self.assertIsNotNone(game.taking_bid)
                self.assertNotEqual(game.taking_bid.get_str(), 'PASSE')
                went_though_dog += 1
                self.assertIn(np.random.choice(game.get_legal_actions()).get_str(), ACTION_LIST)
            if game.current_game_part == 'MAIN' and not game.is_over():
                went_though_main += 1
                self.assertIn(np.random.choice(game.get_legal_actions()).get_str(), ACTION_LIST)
        nb_taking = 0
        for player_id in range(game.num_players):
            if game.players[player_id].taking:
                nb_taking += 1
        self.assertEqual(nb_taking, 1)
        if game.taking_bid < 4:
            self.assertEqual(went_though_dog, game.num_cards_dog)
        else:
            self.assertEqual(went_though_dog, 0)
        self.assertEqual(went_though_main, 72)

    def test_final_payoff(self):
        game = GlobalGame()
        game.init_game()
        while not game.is_over():
            action = np.random.choice(game.get_legal_actions())
            _, _ = game.step(action)
        payoffs = game.get_payoffs()
        print(payoffs)
        self.assertEqual(len(payoffs), game.num_players)
        self.assertNotEqual(payoffs[random.randint(0, game.num_players - 1)], 0)


if __name__ == '__main__':
    unittest.main()
