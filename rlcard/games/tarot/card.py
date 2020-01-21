class TarotCard(object):
    info = {'is_trump': [True, False],
            'color': ['SPADE', 'CLOVER', 'HEART', 'DIAMOND'],
            'color_value': range(1, 15),
            'trump_value': range(0, 22)
            }

    def __init__(self, is_trump, color='SPADE', color_value=1, trump_value=0):
        ''' Initialize the class of TarotCard

        Args:
            is_trump (str): The type of card
            color (str): The color of card
            color_value (int): The value of card
            trump_value (int): The value of card when trump
        '''
        self.is_trump = is_trump
        self.color = color
        self.color_value = color_value
        self.trump_value = trump_value
        self.str = self.get_str()

    def get_str(self):
        ''' Get the string representation of card

        Return:
            (str): The string of card's color and value
        '''
        if self.is_trump:
            return 'Trump-' + str(self.trump_value)
        else:
            return self.color + '-' + str(self.value)

    @staticmethod
    def print_cards(cards):  # TODO : understand how to work with a static method - unused for now
        ''' Print out card in a nice form

        Args:
            card (str or list): The string form or a list of tarot card
        '''
        if isinstance(cards, str):
            cards = [cards]
        for i, card in enumerate(cards):
            color, value = card.split('-')
            print(value, ' of ', color)

            if i < len(cards) - 1:
                print(', ', end='')
