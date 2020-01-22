class TarotBid(object):
    order = {'PASSE': 0,
             'PETITE': 1,
             'POUSSE': 2,
             'GARDE': 3,
             'GARDE_SANS': 4,
             'GARDE_CONTRE': 5}

    value = {'PASSE': 0,
             'PETITE': 1,
             'POUSSE': 2,
             'GARDE': 4,
             'GARDE_SANS': 8,
             'GARDE_CONTRE': 16}

    def __init__(self, bid: str):
        self.bid = bid

    def get_bid_order(self):
        """

        :return: bid value
        """
        return TarotBid.order[self.bid]

    def get_bid_value(self):
        """

        :return: bid value
        """
        return TarotBid.value[self.bid]
