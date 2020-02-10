"""
An example of learning a Deep-Q Agent on French Tarot Game
"""
import os

import tensorflow as tf

import rlcard
from rlcard.agents.random_agent import RandomAgent
from rlcard.games.tarot.utils import get_hand_value, get_nb_bouts
from rlcard.models.pretrained_models_tarot_v_ import TarotDQNModelV1
from rlcard.utils.logger import Logger

num_tests = 100000
num_games = 2000
stats_on_model = 0
models = {'0': RandomAgent, '1': TarotDQNModelV1}

# Model save path
save_path = 'examples/statistics/tarot_v{}/'.format(str(stats_on_model))
if not os.path.exists('examples/statistics'):
    os.makedirs('examples/statistics')
    if not os.path.exists(save_path):
        os.makedirs(save_path)

csv_path_taking = save_path + 'taking_stats.csv'

logger_taking = Logger(xlabel='hand_value', ylabel='nb_bouts', zlabel='taking_bid_order', legend='',
                       csv_path=csv_path_taking)

csv_path_game = save_path + 'games_stats.csv'

logger_game = Logger(
    label_list=['game_id', 'hand_value', 'nb_bouts', 'nb_bouts_dog', 'taking', 'taking_bid_order',
                'number_of_points_achieved',
                'nb_bouts_achieved', 'reward'],
    legend='',
    csv_path=csv_path_game)

# Testing bid strategy of this agent
with tf.compat.v1.Session() as sess:
    # Make environment
    env = rlcard.make('tarot')
    # Set agents
    if stats_on_model == 0:
        agent = models[str(stats_on_model)](env.game.get_action_num())
    else:
        agent = models[str(stats_on_model)](sess.graph, sess).dqn_agent
    global_step = tf.Variable(0, name='global_step', trainable=False)
    sess.run(tf.compat.v1.global_variables_initializer())

    # STATS ON TAKING BID FOR FIRST PLAYER TO SPEAK
    print('\n------------------------')
    print('---- Stats on Bids -----')
    print('------------------------')
    for i in range(num_tests):
        if i * 100 % num_tests == 0:
            print('\rProgress Bids: {}%'.format(int(i * 100 / num_tests)), end='')
        state, player_id = env.init_game()
        points_in_hand = get_hand_value(env.game.players[player_id].hand)
        bouts_in_hand = get_nb_bouts(env.game.players[player_id].hand)
        action = env.decode_action(agent.step(state))
        logger_taking.add_point(x=points_in_hand, y=bouts_in_hand, z=action.get_bid_order())

    # Showing usual results against himself for this agent
    print('\n------------------------')
    print('---- Stats on Games ----')
    print('------------------------')
    # Make environment
    env = rlcard.make('tarot')
    global_step = tf.Variable(0, name='global_step', trainable=False)
    sess.run(tf.compat.v1.global_variables_initializer())
    for i in range(num_games):
        hand_value = dict()
        nb_bouts = dict()
        initial_hand = dict()
        # PRINTS HERE TO FORCE THE CODE TO CONTINUE (WEIRD PROBLEM IS NOTHING IS ASKED TO BE PRINTED HERE)
        if (i * 1000) % num_games == 0:
            print('\rProgress Games: {}%'.format(round(i * 100 / num_games, 2)), end='')

        state, player_id = env.init_game()
        bid_iteration = 0
        while not env.is_over():
            if env.game.current_game_part == 'BID':
                if bid_iteration % env.player_num == 0:
                    dog_bouts = get_nb_bouts(env.game.dog.hand)
                    for player_id in range(0, env.game.get_player_num()):
                        hand_value[player_id] = get_hand_value(env.game.players[player_id].hand)
                        nb_bouts[player_id] = get_nb_bouts(env.game.players[player_id].hand)
                        initial_hand[player_id] = env.game.players[player_id].hand
                bid_iteration += 1
            action = agent.step(state)
            state, player_id = env.step(action)
        payoffs = env.get_payoffs()
        for player_id in range(0, env.game.get_player_num()):
            if player_id == env.game.taking_player_id:
                taking = 1
                taking_bid_order = env.game.taking_bid_order
            else:
                taking = 0
                bid_or_None = env.game.players[player_id].bid
                if bid_or_None is not None:
                    taking_bid_order = bid_or_None.get_bid_order()
                else:
                    taking_bid_order = 0
            number_of_points_achieved = env.game.players[player_id].points
            nb_bouts_achieved = env.game.players[player_id].bouts
            reward = payoffs[player_id]
            logger_game.add_point(
                write_list=[i, hand_value[player_id], nb_bouts[player_id], dog_bouts, taking, taking_bid_order,
                            number_of_points_achieved, nb_bouts_achieved, reward])
