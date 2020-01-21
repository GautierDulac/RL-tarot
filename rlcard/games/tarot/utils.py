import rlcard

from rlcard.games.tarot.card import TarotCard as Card

# Read required docs
ROOT_PATH = rlcard.__path__[0]


def init_deck():
    """ Generate tarot deck of 78 cards
    """
    deck = []
    card_info = Card.info
    for color in card_info['color']:

        # init number cards
        for num in card_info['color_value']:
            deck.append(Card('number', color, num))

        # init trump cards
        for num in card_info['trump_value']:
            deck.append(Card('trump', color, num))

    return deck


def cards2list(cards):
    """ Get the corresponding string representation of cards

    Args:
        cards (list): list of TarotCards objects

    Returns:
        (string): string representation of cards
    """
    cards_list = []
    for card in cards:
        cards_list.append(card.get_str())
    return cards_list


def hand2dict(hand):
    """ Get the corresponding dict representation of hand

    Args:
        hand (list): list of string of hand's card

    Returns:
        (dict): dict of hand
    """
    hand_dict = {}
    for card in hand:
        if card not in hand_dict:
            hand_dict[card] = 1
        else:
            hand_dict[card] += 1
    return hand_dict
