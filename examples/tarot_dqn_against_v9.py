"""
An example of learning a Deep-Q Agent on French Tarot Game
"""
import os
import time

import tensorflow as tf

import rlcard
from rlcard.models.pretrained_models_tarot_v9 import TarotDQNModelV9
from rlcard.utils.logger import Logger
from rlcard.utils.utils import set_global_seed, time_difference_good_format

record_number = 10

# Make environment
env = rlcard.make('tarot')
eval_env = rlcard.make('tarot')

# Set the iterations numbers and how frequently we evaluate/save plot
evaluate_every = 5
save_plot_every = 100
evaluate_num = 25

episode_num = 1000

# Set the the number of steps for collecting normalization statistics
# and intial memory size
memory_init_size = 1000
norm_step = 100

# The paths for saving the logs and learning curves
root_path = './experiments/tarot_dqn_result_v{}/'.format(str(record_number))
log_path = root_path + 'log.txt'
csv_path = root_path + 'performance.csv'
figure_path = root_path + 'figures/'

# Model save path
if not os.path.exists('rlcard/models'):
    os.makedirs('rlcard/models')
    if not os.path.exists('rlcard/models/pretrained'):
        os.makedirs('rlcard/models/pretrained')
        if not os.path.exists('rlcard/models/pretrained/tarot_v' + str(record_number)):
            os.makedirs('rlcard/models/pretrained/tarot_v' + str(record_number))
model_path = 'rlcard/models/pretrained/tarot_v' + str(record_number) + '/model'

# Set a global seed
set_global_seed(0)

with tf.compat.v1.Session() as sess:
    # Set agents
    global_step = tf.Variable(0, name='global_step', trainable=False)
    agent = TarotDQNModelV9(sess.graph, sess).dqn_agent

    opponent_agent = agent

    sess.run(tf.compat.v1.global_variables_initializer())

    saver = tf.compat.v1.train.Saver()

    env.set_agents([agent] + [opponent_agent] * (env.player_num - 1))
    eval_env.set_agents([agent] + [opponent_agent] * (env.player_num - 1))

    # Count the number of steps
    step_counter = 0

    # Init a Logger to plot the learning curve
    logger = Logger(xlabel='timestep', ylabel='reward', legend='DQN on TAROT', log_path=log_path, csv_path=csv_path)

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

        # Evaluate the performance. Play with random agents.
        if episode % evaluate_every == 0:
            # Save Model
            saver.save(sess, model_path)
            reward = 0
            for eval_episode in range(evaluate_num):
                print('\rEPISODE {} - Eval {} over {} - Number of game played {} - {}'.format(episode, eval_episode,
                                                                                              evaluate_num,
                                                                                              total_game_played,
                                                                                              time_difference_good_format(
                                                                                                  seconds,
                                                                                                  time.time())),
                      end='')
                _, payoffs = eval_env.run(is_training=False)
                total_game_played += 1
                reward += payoffs[0]

            logger.log('\n########## Evaluation - Episode {} ##########'.format(episode))
            logger.log('Timestep: {} Average reward is {}'.format(env.timestep, float(reward) / evaluate_num))

            # Add point to logger
            logger.add_point(x=env.timestep, y=float(reward) / evaluate_num)

        # Make plot
        if episode % save_plot_every == 0 and episode > 0:
            logger.make_plot(save_path=figure_path + str(episode) + '.png')

    # Make the final plot
    logger.make_plot(save_path=figure_path + 'final_' + str(episode) + '.png')
