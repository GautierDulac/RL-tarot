class TarotCard(object):
    info = {'color': ['SPADE', 'CLOVER', 'HEART', 'DIAMOND', 'TRUMP'],
            'value': ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14',
                      '15', '16', '17', '18', '19', '20', '21']
            }

    def __init__(self, color, value):
        ''' Initialize the class of TarotCard

        Args:
            card_type (str): The type of card
            color (str): The color of card
            value (str): The value of card
        '''
        self.color = color
        self.value = value
        self.str = self.get_str()

    def get_str(self):
        ''' Get the string representation of card

        Return:
            (str): The string of card's color and value
        '''
        return self.color + '-' + self.value

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
