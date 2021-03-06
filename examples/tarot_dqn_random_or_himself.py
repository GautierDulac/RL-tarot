"""
An example of learning a Deep-Q Agent on French Tarot Game
"""
import os
import time

import tensorflow as tf

import rlcard
from rlcard.agents.dqn_agent import DQNAgent
from rlcard.agents.random_agent import RandomAgent
from rlcard.utils.logger import Logger
from rlcard.utils.utils import time_difference_good_format

record_number = 15

# Make environment
env = rlcard.make('tarot')
eval_env = rlcard.make('tarot')

# Set the iterations numbers and how frequently we evaluate/save plot
evaluate_every = 100
evaluate_num = 1000
episode_num = 100000
# Train against
train_against = 'random'  # or 'same'

# Set the the number of steps for collecting normalization statistics
# and intial memory size
memory_init_size = 5000
norm_step = 1000

# The paths for saving the logs and learning curves
root_path = './experiments/{}_played_{}/'.format(train_against, str(record_number))
log_path_random = root_path + 'log_random.txt'
csv_path_random = root_path + 'performance_random.csv'
figure_path_random = root_path + 'figures_random/'

log_path_parameters = root_path + 'log_parameters.txt'



# Model save path
if not os.path.exists('rlcard/models'):
    os.makedirs('rlcard/models')
if not os.path.exists('rlcard/models/pretrained'):
    os.makedirs('rlcard/models/pretrained')
for eval_number in range(1, episode_num // evaluate_every + 1):
    model_folder_path = 'rlcard/models/pretrained/{}_played_{}/tarot_v{}'.format(train_against,
                                                                                 str(record_number),
                                                                                 str(
                                                                                     record_number * 10000 + eval_number))
    if not os.path.exists(model_folder_path):
        os.makedirs(model_folder_path)
model_path = 'rlcard/models/pretrained/{}_played_{}/tarot_v{}/model'.format(train_against,
                                                                            str(record_number),
                                                                            str(record_number * 10000))
# Init a Logger to plot the learning curve against random
logger_random = Logger(xlabel='episode', ylabel='reward', legend='DQN on TAROT against Random',
                       legend_hist='Histogram of last evaluations against Random', log_path=log_path_random,
                       csv_path=csv_path_random)

param_file = open(log_path_parameters, 'w')
param_file.write('record_number: {}'.format(record_number) + '\n')
param_file.write('evaluate_every: {}'.format(evaluate_every) + '\n')
param_file.write('evaluate_num: {}'.format(evaluate_num) + '\n')
param_file.write('episode_num: {}'.format(episode_num) + '\n')
param_file.write('train_against: {}'.format(train_against) + '\n')
param_file.write('memory_init_size: {}'.format(memory_init_size) + '\n')
param_file.write('norm_step: {}'.format(norm_step) + '\n')
param_file.flush()
param_file.close()

random_agent = RandomAgent(action_num=78)

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

    sess.run(tf.compat.v1.global_variables_initializer())

    saver = tf.compat.v1.train.Saver(max_to_keep=None)
    if train_against == 'random':
        env.set_agents([agent] + [random_agent] * (env.player_num - 1))
    else:
        env.set_agents([agent] + [agent] * (env.player_num - 1))

    eval_env.set_agents([agent] + [random_agent] * (env.player_num - 1))

    # Count the number of steps
    step_counter = 0



    total_game_played = 0
    seconds = time.time()

    for episode in range(episode_num):
        # Evaluate the performance.
        if episode % evaluate_every == 0:
            # Save Model

            model_path = 'rlcard/models/pretrained/{}_played_{}/tarot_v{}/model'.format(train_against,
                                                                                        str(record_number),
                                                                                        str(
                                                                                            record_number * 10000 + episode // evaluate_every))

            saver.save(sess, model_path)

            # Eval against random
            reward_random = 0
            reward_random_list = []
            taking_list = []
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
            logger_random.add_point(x=episode, y=float(reward_random) / evaluate_num)

            # Make plot
            logger_random.make_plot(save_path=figure_path_random + str(episode) + '.png')
            logger_random.make_plot_hist(save_path_1=figure_path_random + str(episode) + '_hist.png',
                                         save_path_2=figure_path_random + str(episode) + '_freq.png',
                                         reward_list=reward_random_list, taking_list=taking_list)

        print('\rEPISODE {} - Number of game played {} - {}'.format(episode, total_game_played,
                                                                    time_difference_good_format(seconds,
                                                                                                time.time())),
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

    # Make the final plot
    logger_random.make_plot(save_path=figure_path_random + 'final_' + str(episode) + '.png')
    logger_random.make_plot_hist(save_path_1=figure_path_random + str(episode) + '_hist.png',
                                 save_path_2=figure_path_random + str(episode) + '_freq.png',
                                 reward_list=reward_random_list, taking_list=taking_list)
