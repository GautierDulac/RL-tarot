"""
An example of learning a Deep-Q Agent on French Tarot Game
"""
import os
import time

import tensorflow as tf

import rlcard
from rlcard.agents.random_agent import RandomAgent
from rlcard.agents.dqn_agent import DQNAgent
from rlcard.utils.logger import Logger
from rlcard.utils.utils import set_global_seed, time_difference_good_format

record_number = 5

# Make environment
env = rlcard.make('tarot')
eval_env = rlcard.make('tarot')

# Set the iterations numbers and how frequently we evaluate/save plot
evaluate_every = 100
# save_plot_every = 100
evaluate_num = 1000

episode_num = 100000

self_play = 1
total_self_play_eval = int(episode_num / evaluate_every)

# Set the the number of steps for collecting normalization statistics
# and intial memory size
memory_init_size = 1000000
norm_step = 1000

# The paths for saving the logs and learning curves
root_path = './experiments/tarot_dqn_self_played_v{}/'.format(str(record_number))
log_path_random = root_path + 'log_random.txt'
csv_path_random = root_path + 'performance_random.csv'
log_path_opponent = root_path + 'log_opponent.txt'
csv_path_opponent = root_path + 'performance_opponent.csv'
figure_path_random = root_path + 'figures_random/'
figure_path_opponent = root_path + 'figures_opponent/'

# Model save path
if not os.path.exists('rlcard/models'):
    os.makedirs('rlcard/models')
if not os.path.exists('rlcard/models/pretrained'):
    os.makedirs('rlcard/models/pretrained')
for self_play_init in range(1, total_self_play_eval + 1):
    model_folder_path = 'rlcard/models/pretrained/self_played_{}/tarot_v{}'.format(
        str(record_number),
        str(record_number * 10000 + self_play_init))
    if not os.path.exists(model_folder_path):
        os.makedirs(model_folder_path)
model_path = 'rlcard/models/pretrained/self_played_{}/tarot_v{}/model'.format(
    str(record_number),
    str(record_number * 10000 + self_play))

# Set a global seed
set_global_seed(0)

random_agent = RandomAgent(action_num=eval_env.action_num)

with tf.compat.v1.Session() as sess:
    # Set agents
    global_step = tf.Variable(0, name='global_step', trainable=False)
    agent = DQNAgent(sess,
                     scope='dqn',
                     action_num=78,  # env.action_num,
                     replay_memory_size=20000,
                     replay_memory_init_size=memory_init_size,
                     norm_step=norm_step,
                     state_shape=env.state_shape,
                     mlp_layers=[512, 1024, 512])

    opponent_agent = agent

    sess.run(tf.compat.v1.global_variables_initializer())

    saver = tf.compat.v1.train.Saver()

    env.set_agents([agent] + [opponent_agent] * (env.player_num - 1))
    eval_env.set_agents([agent] + [random_agent] * (env.player_num - 1))

    # Count the number of steps
    step_counter = 0

    # Init a Logger to plot the learning curve against random
    logger_random = Logger(xlabel='timestep', ylabel='reward', legend='DQN on TAROT against Random',
                           legend_hist='Histogram of last evaluations against Random', log_path=log_path_random,
                           csv_path=csv_path_random)
    # Init a Logger to plot the learning curve against last opponent
    logger_opponent = Logger(xlabel='timestep', ylabel='reward', legend='DQN on TAROT against last agent',
                             legend_hist='Histogram of last evaluations against last agent', log_path=log_path_opponent,
                             csv_path=csv_path_opponent)

    total_game_played = 0
    seconds = time.time()

    for episode in range(episode_num):
        print('\rEPISODE {} - Number of game played {} - {}'.format(episode, total_game_played,
                                                                    time_difference_good_format(seconds, time.time())),
              end='')

        # Generate data from the environment
        trajectories, _ = env.run(is_training=True)
        total_game_played += 1

        # Feed transitions into agent memory, and train the agent
        for ts in trajectories[0]:
            agent.feed(ts)
            step_counter += 1

            # Train the agent
            train_count = step_counter - (memory_init_size + norm_step)
            if train_count > 0:
                loss = agent.train()
                # print('\rINFO - Step {}, loss: {}'.format(step_counter, loss), end='')

        # Evaluate the performance.
        if episode % evaluate_every == 0:
            # Save Model
            model_path = 'rlcard/models/pretrained/self_played_{}/tarot_v{}/model'.format(
                str(record_number),
                str(record_number * 10000 + self_play))

            saver.save(sess, model_path)

            # Eval against random
            reward_random = 0
            reward_random_list = []
            taking_list = []
            eval_env.set_agents([agent] + [random_agent] * (env.player_num - 1))
            for eval_episode in range(evaluate_num):
                print('\rEPISODE {} - Eval Random {} over {} - Number of game played {} - {}'.format(episode,
                                                                                                     eval_episode,
                                                                                                     evaluate_num,
                                                                                                     total_game_played,
                                                                                                     time_difference_good_format(
                                                                                                         seconds,
                                                                                                         time.time())),
                      end='')
                _, payoffs = eval_env.run(is_training=False)
                total_game_played += 1
                reward_random_list.append(payoffs[0])
                reward_random += payoffs[0]
                taking_list.append(eval_env.game.players[0].taking)

            logger_random.log('\n########## Evaluation Against Random - Episode {} ##########'.format(episode))
            logger_random.log(
                'Timestep: {} Average reward against random is {}'.format(env.timestep,
                                                                          float(reward_random) / evaluate_num))

            # Add point to logger
            logger_random.add_point(x=env.timestep, y=float(reward_random) / evaluate_num)

            # Make plot
            logger_random.make_plot(save_path=figure_path_random + str(episode) + '.png')
            logger_random.make_plot_hist(save_path_1=figure_path_random + str(episode) + '_hist.png',
                                         save_path_2=figure_path_random + str(episode) + '_freq.png',
                                         reward_list=reward_random_list, taking_list=taking_list)

            # Eval against last agent
            reward_opponent = 0
            reward_opponent_list = []
            taking_list = []
            eval_env.set_agents([agent] + [opponent_agent] * (env.player_num - 1))
            for eval_episode in range(evaluate_num):
                print('\rEPISODE {} - Eval Opponent {} over {} - Number of game played {} - {}'.format(episode,
                                                                                                       eval_episode,
                                                                                                       evaluate_num,
                                                                                                       total_game_played,
                                                                                                       time_difference_good_format(
                                                                                                           seconds,
                                                                                                           time.time())),
                      end='')
                _, payoffs = eval_env.run(is_training=False)
                total_game_played += 1
                reward_opponent_list.append(payoffs[0])
                reward_opponent += payoffs[0]
                taking_list.append(eval_env.game.players[0].taking)

            logger_opponent.log('\n########## Evaluation Against Last Agent - Episode {} ##########'.format(episode))
            logger_opponent.log(
                'Timestep: {} Average reward against last agent is {}'.format(env.timestep,
                                                                              float(reward_opponent) / evaluate_num))

            # Add point to logger
            logger_opponent.add_point(x=env.timestep, y=float(reward_opponent) / evaluate_num)

            # Make plot
            logger_opponent.make_plot(save_path=figure_path_opponent + str(episode) + '.png')
            logger_opponent.make_plot_hist(save_path_1=figure_path_opponent + str(episode) + '_hist.png',
                                           save_path_2=figure_path_opponent + str(episode) + '_freq.png',
                                           reward_list=reward_opponent_list, taking_list=taking_list)

            # GO to next step
            self_play += 1

            opponent_agent = agent
            env.set_agents([agent] + [opponent_agent] * (env.player_num - 1))

    # Make the final plot
    logger_random.make_plot(save_path=figure_path_random + 'final_' + str(episode) + '.png')
    logger_random.make_plot_hist(save_path_1=figure_path_random + str(episode) + '_hist.png',
                                 save_path_2=figure_path_random + str(episode) + '_freq.png',
                                 reward_list=reward_random_list)
    # Make the final plot
    logger_opponent.make_plot(save_path=figure_path_opponent + 'final_' + str(episode) + '.png')
    logger_opponent.make_plot_hist(save_path_1=figure_path_opponent + str(episode) + '_hist.png',
                                   save_path_2=figure_path_opponent + str(episode) + '_freq.png',
                                   reward_list=reward_opponent_list)
