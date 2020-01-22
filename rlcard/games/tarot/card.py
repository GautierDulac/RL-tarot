# CLEAR


class TarotCard(object):
    info = {'is_trump': [True, False],
            'color': ['SPADE', 'CLOVER', 'HEART', 'DIAMOND'],
            'color_value': range(1, 15),
            'trump_value': range(0, 22)
            }

    def __init__(self, is_trump, color=None, color_value=None, trump_value=None):
        """ Initialize the class of TarotCard

        Args:
            color (str): The color of card
            color_value (int): The value of card
            trump_value (int): The value of card when trump
        """
        self.is_trump = is_trump
        self.color = color
        self.color_value = color_value
        self.trump_value = trump_value
        self.str = self.get_str()

    def get_str(self):
        """ Get the string representation of card

        Return:
            (str): The string of card's color and value
        """
        if self.is_trump:
            return 'TRUMP-' + str(self.trump_value)
        else:
            return self.color + '-' + str(self.color_value)

    def get_value(self):
        """

        :return: points value of the card (float)
        """
        if self.is_trump:
            if self.trump_value in [0, 1, 21]:
                return 4.5
            else:
                return 0.5
        else:
            if self.color_value <= 10:
                return 0.5
            else:
                return 0.5 + self.color_value - 10

    def is_bout(self):
        """

        :return: Boolean telling if it is "Le Petit", "L'Excuse" ou "Le 21"
        """
        if self.is_trump:
            if self.trump_value in [0, 1, 21]:
                return True
        return False

    @staticmethod
    def print_cards(cards):  # TODO : P2 - understand how to work with a static method - unused for now
        """ Print out card in a nice form

        Args:
            :param cards: (str or list)list of cards to be printed - or string form of tarot card
        """
        if cards is None:
            print('No card played yet')
            return
        if isinstance(cards, str):
            cards = [cards]
        for i, card in enumerate(cards):
            color, value = card.split('-')
            print(value, ' of ', color, end='')

            if i < len(cards) - 1:
                print(', ', end='')
