from typing import List

import numpy as np

from rlcard.games.tarot.alpha_and_omega.card import TarotCard
from rlcard.games.tarot.alpha_and_omega.player import TarotPlayer
from rlcard.games.tarot.utils import get_pot_value, get_nb_bouts


class TarotJudger(object):

    @staticmethod
    def judge_winner(players: List[TarotPlayer], new_dog: List[TarotCard]) -> List[int]:
        """
        Judge the winner of the game
        :param players: All the competing players, a list of TarotPlayer objects
        :param new_dog: A list with the new_dog (possibly the initial one if GARDE_SANS or GARDE_CONTRE)
        :return: a list with all (1 or 3) the winners
        """
        counts = dict()
        for player_id in range(len(players)):
            counts[player_id] = np.sum(players[player_id].points)
            if players[player_id].taking:
                if players[player_id].bid.get_bid_order() <= 4:
                    counts[player_id] += get_pot_value(new_dog)
                    number_bouts = players[player_id].bouts + get_nb_bouts(new_dog)
                else:
                    number_bouts = players[player_id].bouts
                if (number_bouts == 3 and counts[player_id] >= 36) \
                        or (number_bouts == 2 and counts[player_id] >= 41) \
                        or (number_bouts == 1 and counts[player_id] >= 51) \
                        or (number_bouts == 0 and counts[player_id] >= 61):
                    return [player_id]
        all_other_players = [player_id for player_id in range(len(players)) if not players[player_id].taking]
        return all_other_players
