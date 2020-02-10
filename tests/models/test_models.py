import unittest

from rlcard.models.model import Model
from rlcard.models.pretrained_models_tarot_v_ import TarotDQNModelV1
import tensorflow as tf


class TestModel(unittest.TestCase):

    def test_model(self):
        model = Model()
        self.assertIsInstance(model, Model)

    def test_tarot_dqn_model(self):
        with tf.compat.v1.Session() as sess:
            model = TarotDQNModelV1(sess.graph, sess)
            self.assertIsInstance(model, TarotDQNModelV1)


if __name__ == '__main__':
    unittest.main()
