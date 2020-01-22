import unittest

from rlcard.models.model import Model
#from rlcard.models.pretrained_models import LeducHoldemNFSPModel
#TODO : Add pretrained TAROT model for unittest

class TestModel(unittest.TestCase):

    def test_model(self):
        model = Model()
        self.assertIsInstance(model, Model)

#    def test_leduc_holdem_nfsp_model(self):
#        model = LeducHoldemNFSPModel()
#        self.assertIsInstance(model, LeducHoldemNFSPModel)


if __name__ == '__main__':
    unittest.main()
