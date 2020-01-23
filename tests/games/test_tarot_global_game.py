import unittest
import numpy as np
import random

from rlcard.games.tarot.global_game import GlobalGame
from rlcard.games.tarot.bid.bid_game import BidGame
from rlcard.games.tarot.alpha_and_omega.player import TarotPlayer as Player
from rlcard.games.tarot.alpha_and_omega.card import TarotCard as Card
from rlcard.games.tarot.dog.dog import TarotDog
from rlcard.games.tarot.bid.bid import TarotBid
from rlcard.games.tarot.utils import ACTION_LIST
from rlcard.games.tarot.utils import hand2dict, encode_hand, encode_target, get_TarotCard_from_str


class TestTarotMainGameMethods(unittest.TestCase):
    def test_is_over(self):
        game = GlobalGame()
        game.init_game()
        self.assertIsInstance(game.is_over, bool)

    def test_global_over(self):
        game = GlobalGame()
        game.init_game()
        for step_i in range(10000):
            action = np.random.choice(game.get_legal_actions())
            state, _ = game.step(action)
            self.assertEqual(game.is_over, game.bid_over and game.dog_over and game.main_over)
            self.assertEqual(len(game.players[0].hand), game.num_cards_per_player)
            self.assertEqual(len(state['hand']), game.num_cards_per_player)

    def test_global_game(self):
        game = GlobalGame()
        game.init_game()
        went_though_bid = 0
        went_though_dog = 0
        went_though_main = 0
        iteration = 0
        while not game.is_over and iteration < 200:
            iteration += 1
            action = np.random.choice(game.get_legal_actions())
            state, _ = game.step(action)
            action = np.random.choice(game.get_legal_actions())
            if game.current_game_part == 'BID':
                print(action.get_str()) # TODO REMOVE
                went_though_bid += 1
                self.assertIn(action.get_str(), TarotBid.order.keys())
            if game.current_game_part == 'DOG':
                went_though_dog += 1
                self.assertIn(action.get_str(), ACTION_LIST)
            if game.current_game_part == 'MAIN':
                went_though_main += 1
                self.assertIn(action.get_str(), ACTION_LIST)
        self.assertIn(went_though_bid, range(1, 73))
        self.assertEqual(went_though_dog, game.num_cards_dog)
        self.assertEqual(went_though_main, 72)


if __name__ == '__main__':
    unittest.main()
