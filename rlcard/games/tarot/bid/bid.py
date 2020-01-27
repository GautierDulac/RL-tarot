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
        self.str = bid

    def get_str(self) -> str:
        """
        :return: string representation of the bid
        """
        return self.bid

    def get_bid_order(self) -> int:
        """
        :return: bid order (from 0 to 5) - int
        """
        return TarotBid.order[self.bid]

    def get_bid_value(self) -> int:
        """
        :return: bid value (from 0 to 16)
        """
        return TarotBid.value[self.bid]
