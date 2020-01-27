# CLEAR

import numpy as np

from rlcard.games.tarot.utils import get_pot_value


class TarotJudger(object):

    @staticmethod
    def judge_winner(players, new_dog):
        """ Judge the winner of the game

        Args:
            players (list): The list of players who play the game

        Returns:
            (list): The player id of the winner
            :param players:
            :param new_dog:
        """
        counts = dict()
        for player_id in range(len(players)):
            counts[player_id] = np.sum(players[player_id].points)
            if players[player_id].taking:
                if players[player_id].bid.get_bid_order() <= 4:
                    counts[player_id] += get_pot_value(new_dog)
                number_bouts = players[player_id].bouts
                if (number_bouts == 3 and counts[player_id] >= 36) \
                        or (number_bouts == 2 and counts[player_id] >= 41) \
                        or (number_bouts == 1 and counts[player_id] >= 51) \
                        or (number_bouts == 0 and counts[player_id] >= 61):
                    return [player_id]
        all_other_players = [player_id for player_id in range(len(players)) if not players[player_id].taking]
        return all_other_players
