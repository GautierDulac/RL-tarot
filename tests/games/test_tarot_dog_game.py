import unittest
import numpy as np
import random

from rlcard.games.tarot.dog.dog_game import DogGame
from rlcard.games.tarot.alpha_and_omega.player import TarotPlayer as Player
from rlcard.games.tarot.dog.dog import TarotDog
from rlcard.games.tarot.bid.bid_game import BidGame
from rlcard.games.tarot.bid.bid import TarotBid
from rlcard.games.tarot.utils import ACTION_LIST
from rlcard.games.tarot.utils import encode_hand, encode_target

num_players = 4
num_cards_per_player = 18
taking_player_id = random.randint(0, 3)
starting_player = random.randint(0, 3)
players = [Player(i) for i in range(num_players)]
num_cards_dog = 6
dog = TarotDog()

taking_bid = [TarotBid('POUSSE'), TarotBid('GARDE_CONTRE')][random.randint(0, 1)]

bid_game = BidGame(players, num_players, starting_player, num_cards_per_player, num_cards_dog, dog)
bid_game.init_game()

players = bid_game.players
dog = bid_game.dog


class TestTarotBidGameMethods(unittest.TestCase):

    def test_get_action_num(self):
        game = DogGame(players, taking_player_id, num_cards_per_player, num_cards_dog, dog, taking_bid)
        action_num = game.get_action_num()
        self.assertEqual(action_num, 78)

    def test_init_game(self):
        game = DogGame(players, taking_player_id, num_cards_per_player, num_cards_dog, dog, taking_bid)
        state, _ = game.init_game()
        self.assertIn(len(state['others_hand']), [54, 60])
        self.assertEqual(len(state['hand']), game.num_cards_per_player)
        actions = state['legal_actions']
        for action in actions:
            self.assertIn(action.get_str(), ACTION_LIST)

    def test_get_player_id(self):
        game = DogGame(players, taking_player_id, num_cards_per_player, num_cards_dog, dog, taking_bid)
        _, player_id = game.init_game()
        current = game.get_player_id()
        self.assertEqual(player_id, current)

    def test_get_legal_actions(self):
        game = DogGame(players, taking_player_id, num_cards_per_player, num_cards_dog, dog, taking_bid)
        game.init_game()
        actions = game.get_legal_actions()
        for action in actions:
            self.assertIn(action.get_str(), ACTION_LIST)

    def test_step(self):
        game = DogGame(players, taking_player_id, num_cards_per_player, num_cards_dog, dog, taking_bid)
        game.init_game()
        action = np.random.choice(game.get_legal_actions())
        state = game.get_state(taking_player_id)
        total_card = len(list(state['all_cards']))
        state, _ = game.step(action)
        total_card_2 = len(list(state['all_cards']))
        self.assertEqual(total_card - 1, total_card_2)

    def test_get_final_dog(self):
        game = DogGame(players, taking_player_id, num_cards_per_player, num_cards_dog, dog, taking_bid)
        game.init_game()
        state = {}
        while not game.is_over:
            actions = game.get_legal_actions()
            action = np.random.choice(actions)
            state, _ = game.step(action)
            total_cards = len(state['hand'])
            self.assertEqual(total_cards, 18)
        self.assertEqual(len(list(state['new_dog'])), num_cards_dog)

    def test_encode_hand(self):
        # TODO Adapt encode for bid game
        hand1 = ['SPADE-1', 'TRUMP-3', 'DIAMOND-14', 'TRUMP-0', 'TRUMP-21']
        encoded_hand1 = np.zeros((3, 5, 22), dtype=int)
        encode_hand(encoded_hand1, hand1, index_to_encode=0)
        total = 0
        for index in range(22):
            for color in range(5):
                total += encoded_hand1[0][color][index]
        self.assertEqual(total, 5)
        hand2 = hand1
        encoded_hand2 = np.zeros((3, 5, 22), dtype=int)
        encode_hand(encoded_hand2, hand2, index_to_encode=2)
        self.assertEqual(encoded_hand2[2][0][1], 1)  # SPADE-1
        self.assertEqual(encoded_hand2[2][4][0], 1)  # TRUMP-0

    def test_encode_target(self):
        # TODO Adapt
        encoded_target = np.zeros((3, 5, 22), dtype=int)
        target = 'TRUMP-1'
        encode_target(encoded_target[1], target)
        self.assertEqual(encoded_target[1][4][1], 1)


if __name__ == '__main__':
    unittest.main()
