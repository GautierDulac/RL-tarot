"""
An example of learning a Deep-Q Agent on French Tarot Game
"""
import tensorflow as tf
import rlcard
from rlcard.models.pretrained_models_tarot_v_ import TarotDQNModelV1, TarotDQNModelV4, TarotDQNModelV9

against_model = 9
models = {'1': TarotDQNModelV1, '4': TarotDQNModelV4, '9': TarotDQNModelV9}


# Make environment
env = rlcard.make('tarot')

env.set_mode(human_mode=True)

with tf.compat.v1.Session() as sess:
    # Set agents
    global_step = tf.Variable(0, name='global_step', trainable=False)
    agent = models[str(against_model)](sess.graph, sess).dqn_agent
    sess.run(tf.compat.v1.global_variables_initializer())
    state = env.reset()

    while not env.is_over():
        action = agent.step(state)
        state, player_id = env.step(action)
