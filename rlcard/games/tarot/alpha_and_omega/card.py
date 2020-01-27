class TarotCard(object):
    info = {'is_trump': [True, False],
            'color': ['SPADE', 'CLOVER', 'HEART', 'DIAMOND'],
            'color_value': range(1, 15),
            'trump_value': range(0, 22)
            }

    def __init__(self, is_trump: bool, color: str = None, color_value: int = None, trump_value: int = None):
        """
        Initialize the class of TarotCard
        :param is_trump: True if trump color
        :param color: str representation of the color ('SPADE', 'CLOVER', 'HEART', 'DIAMOND')
        :param color_value: int in between 1 and 14
        :param trump_value: int in between 0 and 21
        """
        self.is_trump = is_trump
        self.color = color
        self.color_value = color_value
        self.trump_value = trump_value
        self.str = self.get_str()

    def get_str(self) -> str:
        """
        Get the string representation of card
        :return: A string reprensenting the card
        """
        if self.is_trump:
            return 'TRUMP-' + str(self.trump_value)
        else:
            return self.color + '-' + str(self.color_value)

    def get_value(self) -> float:
        """
        Compute the value of a given card
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

    def is_bout(self) -> bool:
        """
        :return: Boolean telling if it is "Le Petit", "L'Excuse" ou "Le 21"
        """
        if self.is_trump:
            if self.trump_value in [0, 1, 21]:
                return True
        return False

    @staticmethod
    def print_cards(cards) -> None:
        """
        Print out cards in a nice form
        :param cards: (str or list of str) list of cards to be printed - or string form of tarot card
        :return:
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
