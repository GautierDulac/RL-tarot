import unittest
import numpy as np

from rlcard.games.tarot.game import TarotGame as Game
from rlcard.games.tarot.player import TarotPlayer as Player
from rlcard.games.tarot.card import TarotCard as Card
from rlcard.games.tarot.utils import ACTION_LIST
from rlcard.games.tarot.utils import hand2dict, encode_hand, encode_target, get_TarotCard_from_str


class TestTarotMethods(unittest.TestCase):

    def test_get_player_num(self):
        game = Game()
        num_player = game.get_player_num()
        self.assertEqual(num_player, 4)

    def test_get_action_num(self):
        game = Game()
        action_num = game.get_action_num()
        self.assertEqual(action_num, 78)

    def test_init_game(self):
        game = Game()
        state, _ = game.init_game()
        total_cards = list(state['hand'] + state['others_hand'])
        self.assertEqual(len(total_cards), game.num_players*game.num_cards_per_player)

    def test_init_cards(self):
        game = Game()
        state, _ = game.init_game()
        self.assertEqual(len(list(state['hand'])), game.num_cards_per_player)

    def test_get_player_id(self):
        game = Game()
        _, player_id = game.init_game()
        current = game.get_player_id()
        self.assertEqual(player_id, current)

    def test_get_legal_actions(self):
        game = Game()
        game.init_game()
        actions = game.get_legal_actions()
        for action in actions:
            self.assertIn(action.get_str(), ACTION_LIST)

    def test_step(self):
        game = Game()
        game.init_game()
        action = np.random.choice(game.get_legal_actions())
        state, next_player_id = game.step(action)
        current = game.round.current_player_id
        self.assertLessEqual(len(state['played_cards']), 2)
        self.assertEqual(next_player_id, current)

    def test_get_payoffs(self):
        game = Game()
        game.init_game()
        while not game.is_over():
            actions = game.get_legal_actions()
            action = np.random.choice(actions)
            state, _ = game.step(action)
            total_cards = len(state['hand']) + len(state['others_hand']) + len(state['played_cards'])
            self.assertEqual(total_cards, 72)  # Not counting the dog in it
        payoffs = game.get_payoffs()
        total = 0
        for payoff in payoffs:
            total += payoff
        self.assertEqual(total, 0)

    def test_step_back(self):
        game = Game()
        _, player_id = game.init_game()
        action = np.random.choice(game.get_legal_actions())
        self.assertEqual(game.round.current_player_id, player_id)
        game.step(action)
        self.assertEqual(game.round.current_player_id, player_id + 1 % game.num_players)

    def test_hand2dict(self):
        hand_1 = ['SPADE-1', 'TRUMP-3', 'DIAMOND-14', 'TRUMP-0', 'TRUMP-21']
        hand1_dict = hand2dict(hand_1)
        for _, count in hand1_dict.items():
            self.assertEqual(count, 1)

    def test_str_to_card_and_reverse(self):
        card = Card(True, trump_value=10)
        self.assertEqual(get_TarotCard_from_str(card.get_str()).get_str(), card.get_str())
        card = Card(False, color='SPADE', color_value=10)
        self.assertEqual(get_TarotCard_from_str(card.get_str()).get_str(), card.get_str())
        str_card = 'TRUMP-10'
        self.assertEqual(get_TarotCard_from_str(str_card).get_str(), str_card)
        str_card = 'SPADE-10'
        self.assertEqual(get_TarotCard_from_str(str_card).get_str(), str_card)

    def test_encode_hand(self):
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
        encoded_target = np.zeros((3, 5, 22), dtype=int)
        target = 'TRUMP-1'
        encode_target(encoded_target[1], target)
        self.assertEqual(encoded_target[1][4][1], 1)

    def test_player_get_player_id(self):
        player = Player(0)
        self.assertEqual(0, player.get_player_id())


if __name__ == '__main__':
    unittest.main()
