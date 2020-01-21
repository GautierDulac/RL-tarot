import numpy as np

from rlcard.games.tarot.card import TarotCard as Card
from collections import OrderedDict

# a map of color to its index
COLOR_MAP = {'SPADE': 0, 'CLOVER': 1, 'HEART': 2, 'DIAMOND': 3, 'TRUMP': 4}

VALUE_MAP = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7,
             '8': 8, '9': 9, '10': 10, '11': 11, '12': 12, '13': 13, '14': 14,
             '15': 15, '16': 16, '17': 17, '18': 18, '19': 19, '20': 20, '21': 21}


def init_deck():
    """ Generate tarot deck of 78 cards
    """
    card_deck = []
    card_info = Card.info
    for color in card_info['color']:

        # init number cards
        for num in card_info['color_value']:
            card_deck.append(Card(False, color=color, color_value=num))

    # init trump cards
    for num in card_info['trump_value']:
        card_deck.append(Card(True, trump_value=num))

    return card_deck


deck = init_deck()
ACTION_DICT = dict()
for index, a_card in enumerate(deck):
    ACTION_DICT[a_card.str] = index
ACTION_SPACE = OrderedDict(ACTION_DICT)
ACTION_LIST = list(ACTION_SPACE.keys())


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
        hand_dict[card] = 1
    return hand_dict


def encode_hand(plane, hand):
    """ Encode hand and represerve it into plane
    Args:
        plane (array): n*5*22 numpy array
        hand (list): list of string of hand's card
    Returns:
        (array): n*5*22 numpy array
    """
    # TODO : understand full dimension of plane
    # plane = np.zeros((n, 5, 22), dtype=int)
    plane[0] = np.zeros((5, 22), dtype=int)
    for card in hand:
        card_info = card.split('-')
        color = COLOR_MAP[card_info[0]]
        value = VALUE_MAP[card_info[1]]
        plane[0][color][value] = 1
    return plane


def encode_target(plane, target):
    """ Encode target and represerve it into plane
    Args:
        plane (array): n*5*22 numpy array
        target(str): string of target card
    Returns:
        (array): n*5*22 numpy array
    """
    target_info = target.split('-')
    color = COLOR_MAP[target_info[0]]
    value = VALUE_MAP[target_info[1]]
    plane[1][color][value] = 1
    return plane
