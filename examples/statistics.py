"""
An example of learning a Deep-Q Agent on French Tarot Game
"""
import os

import tensorflow as tf

import rlcard
from rlcard.games.tarot.utils import get_hand_value, get_nb_bouts
from rlcard.models.pretrained_models_tarot_v1 import TarotDQNModelV1
from rlcard.utils.logger import Logger

num_tests = 100000
log_limit = 1000
stats_on_model = 1

save_path = 'examples/statistics/tarot_v{}/'.format(str(stats_on_model))
log_path_taking = save_path + 'log.txt'
csv_path_taking = save_path + 'taking_stats.csv'

# Make environment
env = rlcard.make('tarot')

# Model save path
if not os.path.exists('examples/statistics'):
    os.makedirs('examples/statistics')
    if not os.path.exists(save_path):
        os.makedirs(save_path)

logger_taking = Logger(xlabel='hand_value', ylabel='nb_bouts', zlabel='taking_bid_order', legend='',
                       log_path=log_path_taking,
                       csv_path=csv_path_taking)

with tf.compat.v1.Session() as sess:
    # Set agents
    global_step = tf.Variable(0, name='global_step', trainable=False)
    agent = TarotDQNModelV1(sess.graph, sess).dqn_agent
    sess.run(tf.compat.v1.global_variables_initializer())

    records = [[], [], []]
    # STATS ON TAKING BID FOR FIRST PLAYER TO SPEAK
    for i in range(num_tests):
        state, player_id = env.init_game()
        points_in_hand = get_hand_value(env.game.players[player_id].hand)
        records[0].append(points_in_hand)
        bouts_in_hand = get_nb_bouts(env.game.players[player_id].hand)
        records[1].append(bouts_in_hand)
        action = env.decode_action(agent.step(state))
        records[2].append(action.get_bid_order())
        if i < log_limit:
            logger_taking.log(
                'Saying {} with {} points in hand and {} bouts'.format(action.get_str(), points_in_hand, bouts_in_hand))
        logger_taking.add_point(x=points_in_hand, y=bouts_in_hand, z=action.get_bid_order())
