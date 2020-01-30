import unittest

from rlcard.models.model import Model
from rlcard.models.pretrained_models_tarot_v1 import TarotDQNModelV1


class TestModel(unittest.TestCase):

    def test_model(self):
        model = Model()
        self.assertIsInstance(model, Model)

    def test_tarot_dqn_model(self):
        model = TarotDQNModelV1()
        self.assertIsInstance(model, TarotDQNModelV1)


if __name__ == '__main__':
    unittest.main()
