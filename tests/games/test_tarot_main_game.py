import random
import unittest

import numpy as np

from rlcard.games.tarot.alpha_and_omega.card import TarotCard as Card
from rlcard.games.tarot.alpha_and_omega.player import TarotPlayer as Player
from rlcard.games.tarot.bid.bid import TarotBid
from rlcard.games.tarot.bid.bid_game import BidGame
from rlcard.games.tarot.dog.dog import TarotDog
from rlcard.games.tarot.global_game import GlobalGame
from rlcard.games.tarot.main_game.main_game import MainGame
from rlcard.games.tarot.utils import ACTION_LIST, get_end_pot_information, get_nb_bouts
from rlcard.games.tarot.utils import hand2dict, encode_hand, encode_target, get_TarotCard_from_str

num_players = 4
num_cards_per_player = 18
taking_player_id = random.randint(0, 3)
starting_player = random.randint(0, 3)
players = [Player(i) for i in range(num_players)]
num_cards_dog = 6
dog = TarotDog()
taking_bid = [TarotBid('POUSSE'), TarotBid('GARDE_CONTRE')][random.randint(0, 1)]
taking_bid = TarotBid('POUSSE')
players[taking_player_id].bid = taking_bid
players[taking_player_id].taking = True
new_dog = dog.hand


class TestTarotMainGameMethods(unittest.TestCase):
    def test_get_player_num(self):
        game = MainGame(num_players, num_cards_per_player, starting_player, players, taking_player_id, new_dog)
        num_player = game.get_player_num()
        self.assertEqual(num_player, 4)

    def test_get_action_num(self):
        game = MainGame(num_players, num_cards_per_player, starting_player, players, taking_player_id, new_dog)
        action_num = game.get_action_num()
        self.assertEqual(action_num, 78)

    def test_init_game(self):
        bid_game = BidGame(players, num_players, starting_player, num_cards_per_player, num_cards_dog, dog)
        bid_game.init_game()
        game = MainGame(num_players, num_cards_per_player, starting_player, players, taking_player_id, new_dog)
        state, _ = game.init_game()
        total_cards = list(state['hand'] + state['others_hand'])
        self.assertIn(len(total_cards), [game.num_players * game.num_cards_per_player,
                                         game.num_players * game.num_cards_per_player + num_cards_dog])

    def test_init_cards_main(self):
        bid_game = BidGame(players, num_players, starting_player, num_cards_per_player, num_cards_dog, dog)
        bid_game.init_game()
        game = MainGame(num_players, num_cards_per_player, starting_player, players, taking_player_id, new_dog)
        state, _ = game.init_game()
        self.assertEqual(len(list(state['hand'])), game.num_cards_per_player)

    def test_init_cards_global(self):
        game = GlobalGame()
        state, _ = game.init_game()
        self.assertEqual(len(list(state['hand'])), game.num_cards_per_player)

    def test_bid(self):
        bid1 = TarotBid('PASSE')
        bid2 = TarotBid('PETITE')
        self.assertLess(bid1.get_bid_order(), bid2.get_bid_order())

    def test_get_player_id(self):
        game = MainGame(num_players, num_cards_per_player, starting_player, players, taking_player_id, new_dog)
        _, player_id = game.init_game()
        current = game.get_player_id()
        self.assertEqual(player_id, current)

    def test_get_legal_actions(self):
        game = MainGame(num_players, num_cards_per_player, starting_player, players, taking_player_id, new_dog)
        game.init_game()
        actions = game.get_legal_actions()
        for action in actions:
            self.assertIn(action.get_str(), ACTION_LIST)

    def test_step(self):
        bid_game = BidGame(players, num_players, starting_player, num_cards_per_player, num_cards_dog, dog)
        bid_game.init_game()
        game = MainGame(num_players, num_cards_per_player, starting_player, players, taking_player_id, new_dog)
        game.init_game()
        action = np.random.choice(game.get_legal_actions())
        state, next_player_id = game.step(action)
        current = game.main_round.current_player_id
        self.assertLessEqual(len(state['played_cards']), 2)
        self.assertEqual(next_player_id, current)

    def test_get_payoffs_main(self):
        bid_game = BidGame(players, num_players, starting_player, num_cards_per_player, num_cards_dog, dog)
        bid_game.init_game()
        game = MainGame(num_players, num_cards_per_player, starting_player, players, taking_player_id, new_dog)
        game.init_game()
        while not game.is_over:
            actions = game.get_legal_actions()
            action = np.random.choice(actions)
            state, _ = game.step(action)
            print(len(state['hand']))
            print(len(state['others_hand']))
            print(len(state['played_cards']))
            total_cards = len(state['hand']) + len(state['others_hand']) + len(state['played_cards'])
            if game.taking_bid <= 3:
                self.assertEqual(total_cards, 72)  # Not counting the dog in it
            else:
                self.assertEqual(total_cards, 78)  # Adding the dog in the others hand as not known cards
        payoffs = game.get_payoffs()
        total = 0
        for _, payoff in payoffs.items():
            total += payoff
        self.assertEqual(total, 0)

    def test_step_back(self):
        bid_game = BidGame(players, num_players, starting_player, num_cards_per_player, num_cards_dog, dog)
        bid_game.init_game()
        game = MainGame(num_players, num_cards_per_player, starting_player, players, taking_player_id, new_dog)
        _, player_id = game.init_game()
        action = np.random.choice(game.get_legal_actions())
        self.assertEqual(game.main_round.current_player_id, player_id)
        game.step(action)
        self.assertEqual(game.main_round.current_player_id, (player_id + 1) % game.num_players)

    def test_hand2dict(self):
        hand_1 = ['SPADE-1', 'TRUMP-3', 'DIAMOND-14', 'TRUMP-0', 'TRUMP-21']
        hand1_dict = hand2dict(hand_1)
        for _, count in hand1_dict.items():
            self.assertEqual(count, 1)

    def test_str_to_card_and_rev(self):
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
        encoded_target = np.zeros((6, 5, 22), dtype=int)
        target = 'TRUMP-1'
        encode_target(encoded_target, target, index_to_encode=1)
        self.assertEqual(encoded_target[1][4][1], 1)

    def test_player_get_player_id(self):
        player = Player(0)
        self.assertEqual(0, player.get_player_id())

    def test_value_card(self):
        card = Card(True, trump_value=0)
        self.assertEqual(card.get_value(), 4.5)
        card = Card(True, trump_value=2)
        self.assertEqual(card.get_value(), .5)
        card = Card(False, color='SPADE', color_value=12)
        self.assertEqual(card.get_value(), 2.5)
        list_card = [Card(True, trump_value=0),Card(True, trump_value=1),Card(True, trump_value=21)]
        self.assertEqual(get_nb_bouts(list_card),3)

    def test_is_bout(self):
        card = Card(True, trump_value=0)
        self.assertEqual(card.is_bout(), True)
        card = Card(True, trump_value=1)
        self.assertEqual(card.is_bout(), True)
        card = Card(True, trump_value=21)
        self.assertEqual(card.is_bout(), True)
        card = Card(True, trump_value=2)
        self.assertEqual(card.is_bout(), False)

    def test_get_end_pot_info(self):
        pot_cards = {'target': Card(True, trump_value=1), 0: Card(True, trump_value=21),
                     1: Card(True, trump_value=1), 2: Card(True, trump_value=19),
                     3: Card(True, trump_value=20)}
        winner_id, pot_value, nb_bout = get_end_pot_information(pot_cards)
        self.assertEqual(winner_id, 0)
        self.assertEqual(nb_bout, 2)
        self.assertEqual(pot_value, 10)
        pot_cards = {'target': Card(True, trump_value=21), 0: Card(True, trump_value=21),
                     1: Card(True, trump_value=0), 2: Card(True, trump_value=19),
                     3: Card(True, trump_value=1)}
        winner_id, pot_value, nb_bout = get_end_pot_information(pot_cards)
        self.assertEqual(winner_id, 0)
        self.assertEqual(nb_bout, 3)
        self.assertEqual(pot_value, 14)
        pot_cards = {'target': Card(False, color_value=14, color='SPADE'), 0: Card(False, color_value=14, color='SPADE'),
                     1: Card(True, trump_value=0), 2: Card(False, color_value=1, color='SPADE'),
                     3: Card(False, color_value=2, color='SPADE')}
        winner_id, pot_value, nb_bout = get_end_pot_information(pot_cards)
        self.assertEqual(winner_id, 0)
        self.assertEqual(nb_bout, 1)
        self.assertEqual(pot_value, 10)
        pot_cards = {'target': Card(False, color_value=14, color='SPADE'), 0: Card(False, color_value=3, color='SPADE'),
                     1: Card(True, trump_value=0), 2: Card(True, trump_value=1),
                     3: Card(False, color_value=2, color='SPADE')}
        winner_id, pot_value, nb_bout = get_end_pot_information(pot_cards)
        self.assertEqual(winner_id, 2)
        self.assertEqual(nb_bout, 2)
        self.assertEqual(pot_value, 10)
        pot_cards = {'target': Card(False, color_value=14, color='SPADE'), 0: Card(False, color_value=3, color='SPADE'),
                     1: Card(True, trump_value=0), 2: Card(True, trump_value=21),
                     3: Card(False, color_value=2, color='SPADE')}
        winner_id, pot_value, nb_bout = get_end_pot_information(pot_cards)
        self.assertEqual(winner_id, 2)
        self.assertEqual(nb_bout, 2)
        self.assertEqual(pot_value, 10)
        pot_cards = {'target': Card(True, trump_value=20), 0: Card(True, trump_value=20),
                     1: Card(True, trump_value=12), 2: Card(True, trump_value=21),
                     3: Card(True, trump_value=17)}
        winner_id, pot_value, nb_bout = get_end_pot_information(pot_cards)
        self.assertEqual(winner_id, 2)
        self.assertEqual(nb_bout, 1)
        self.assertEqual(pot_value, 6)


if __name__ == '__main__':
    unittest.main()
