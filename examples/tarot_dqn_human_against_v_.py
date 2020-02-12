"""
An example of learning a Deep-Q Agent on French Tarot Game
"""
import tensorflow as tf
import rlcard
from rlcard.models.pretrained_models_tarot_v_ import TarotDQNModelV1, TarotDQNModelV60073

against_model = 60073
models = {'1': TarotDQNModelV1, '60073': TarotDQNModelV60073}


# Make environment
env = rlcard.make('tarot')

env.set_mode(human_mode=True)

with tf.compat.v1.Session() as sess:
    # Set agents
    global_step = tf.Variable(0, name='global_step', trainable=False)
    agent = models[str(against_model)](sess.graph, sess).dqn_agent
    sess.run(tf.compat.v1.global_variables_initializer())
    state = env.reset()
    player_id = env.game.starting_player
    while not env.is_over():
        action = agent.step(state)
        if player_id == 0:
            action = input('Choose an action id') #TODO repair the choice that gives wrong card (kings eg)
        state, player_id = env.step(action)
