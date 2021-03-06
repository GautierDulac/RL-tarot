import unittest
import numpy as np
import random

from rlcard.games.tarot.global_game import GlobalGame
from rlcard.games.tarot.bid.bid_game import BidGame
from rlcard.games.tarot.alpha_and_omega.player import TarotPlayer as Player
from rlcard.games.tarot.dog.dog import TarotDog
from rlcard.games.tarot.bid.bid import TarotBid
from rlcard.games.tarot.utils import encode_hand, encode_target, encode_bid

num_players = 4
num_cards_per_player = 18
starting_player = random.randint(0, 3)
players = [Player(i) for i in range(num_players)]
num_cards_dog = 6
dog = TarotDog()


class TestTarotBidGameMethods(unittest.TestCase):

    def test_get_player_num(self):
        game = BidGame(players, num_players, starting_player, num_cards_per_player, num_cards_dog, dog)
        num_player = game.get_player_num()
        self.assertEqual(num_player, 4)

    def test_get_action_num(self):
        game = BidGame(players, num_players, starting_player, num_cards_per_player, num_cards_dog, dog)
        action_num = game.get_action_num()
        self.assertEqual(action_num, 6)

    def test_init_game(self):
        game = BidGame(players, num_players, starting_player, num_cards_per_player, num_cards_dog, dog)
        state, _ = game.init_game()
        self.assertIsInstance(state['max_bid'], int)
        self.assertEqual(len(state['hand']), game.num_cards_per_player)
        actions = state['legal_actions']
        for action in actions:
            self.assertIn(action.get_str(), TarotBid.order.keys())

    def test_init_cards(self):
        game = GlobalGame()
        state, _ = game.init_game()
        self.assertEqual(len(list(state['hand'])), game.num_cards_per_player)

    def test_bid(self):
        bid1 = TarotBid('PASSE')
        bid2 = TarotBid('PETITE')
        self.assertLess(bid1.get_bid_order(), bid2.get_bid_order())

    def test_get_player_id(self):
        game = BidGame(players, num_players, starting_player, num_cards_per_player, num_cards_dog, dog)
        _, player_id = game.init_game()
        current = game.get_player_id()
        self.assertEqual(player_id, current)

    def test_get_legal_actions(self):
        game = BidGame(players, num_players, starting_player, num_cards_per_player, num_cards_dog, dog)
        game.init_game()
        actions = game.get_legal_actions()
        for action in actions:
            self.assertIn(action.get_str(), TarotBid.order.keys())

    def test_step(self):
        game = BidGame(players, num_players, starting_player, num_cards_per_player, num_cards_dog, dog)
        game.init_game()
        action = np.random.choice(game.get_legal_actions())
        current = game.bid_round.current_player_id
        state, next_player_id = game.step(action)
        self.assertLessEqual(len(state['other_bids']), num_players)
        self.assertEqual(next_player_id, (current + 1) % num_players)

    def test_get_final_bid(self):
        game = BidGame(players, num_players, starting_player, num_cards_per_player, num_cards_dog, dog)
        game.init_game()
        while not game.bid_over:
            actions = game.get_legal_actions()
            action = np.random.choice(actions)
            state, _ = game.step(action)
            total_cards = len(state['hand'])
            self.assertEqual(total_cards, 18)
        taking_player_id = game.bid_round.taking_player_id
        self.assertIsInstance(taking_player_id, int)
        self.assertLessEqual(- game.bid_round.max_bid_order, -1)

    def test_encode_bid(self):
        bids = [TarotBid('PASSE'), TarotBid('PASSE'), TarotBid('GARDE_CONTRE')]
        plane = np.zeros((6, 5, 22), dtype=int)
        encode_bid(plane, bids, index_to_encode='2-0')
        total = 0
        for index1 in range(5):
            for index2 in range(22):
                total += plane[2][index1][index2]
        self.assertEqual(total, 3)
        self.assertEqual(plane[2][0][0], 2)
        self.assertEqual(plane[2][0][5], 1)

    def test_encode_target(self):
        encoded_target = np.zeros((6, 5, 22), dtype=int)
        target = 'TRUMP-1'
        encode_target(encoded_target, target, index_to_encode=2)
        self.assertEqual(encoded_target[2][4][1], 1)


if __name__ == '__main__':
    unittest.main()
