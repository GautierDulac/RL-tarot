"""
An example of learning a Deep-Q Agent on French Tarot Game
"""
import os

import tensorflow as tf

import rlcard
from rlcard.agents.dqn_agent import DQNAgent
from rlcard.agents.random_agent import RandomAgent
from rlcard.utils.logger import Logger
from rlcard.utils.utils import set_global_seed

# Make environment
env = rlcard.make('tarot')
eval_env = rlcard.make('tarot')

# Set the iterations numbers and how frequently we evaluate/save plot
evaluate_every = 25
save_plot_every = 100
evaluate_num = 10
episode_num = 10000

# Set the the number of steps for collecting normalization statistics
# and intial memory size
memory_init_size = 1000
norm_step = 100

# The paths for saving the logs and learning curves
root_path = './experiments/tarot_dqn_result/'
log_path = root_path + 'log.txt'
csv_path = root_path + 'performance.csv'
figure_path = root_path + 'figures/'

# Model save path
if not os.path.exists('models'):
    os.makedirs('models')
    if not os.path.exists('models/tarot'):
        os.makedirs('models/tarot')
        if not os.path.exists('models/tarot/model'):
            os.makedirs('models/tarot/model')
model_path = 'models/tarot/model'

# Set a global seed
set_global_seed(0)

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
                     mlp_layers=[512, 512])

    random_agent = RandomAgent(action_num=eval_env.action_num)

    sess.run(tf.compat.v1.global_variables_initializer())

    saver = tf.compat.v1.train.Saver()

    env.set_agents([agent] + [random_agent] * (env.player_num - 1))
    eval_env.set_agents([agent] + [random_agent] * (env.player_num - 1))

    # Count the number of steps
    step_counter = 0

    # Init a Logger to plot the learning curve
    logger = Logger(xlabel='timestep', ylabel='reward', legend='DQN on TAROT', log_path=log_path, csv_path=csv_path)

    for episode in range(episode_num):

        # Generate data from the environment
        trajectories, _ = env.run(is_training=True)

        # Feed transitions into agent memory, and train the agent
        for ts in trajectories[0]:
            agent.feed(ts)
            step_counter += 1

            # Train the agent
            train_count = step_counter - (memory_init_size + norm_step)
            if train_count > 0:
                loss = agent.train()
                print('\rINFO - Step {}, loss: {}'.format(step_counter, loss), end='')

        # Evaluate the performance. Play with random agents.
        if episode % evaluate_every == 0:
            # Save Model
            saver.save(sess, 'models/tarot/model')
            reward = 0
            for eval_episode in range(evaluate_num):
                _, payoffs = eval_env.run(is_training=False)
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
