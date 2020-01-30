import random
from typing import List

import numpy as np


def reorganize(trajectories: list, payoffs: dict) -> list:
    """
    Reorganize the trajectory to make it RL friendly
    :param trajectories: (list): A list of trajectories
    :param payoffs: (dict): A dict of payoffs for the players. Each entry corresponds to one player
    :return: A new trajectories that can be fed into RL algorithms.
    """
    player_num = len(trajectories)
    new_trajectories = [[] for _ in range(player_num)]

    for player in range(player_num):
        for i in range(0, len(trajectories[player]) - 2, 2):
            if i == len(trajectories[player]) - 3:
                reward = payoffs[player]
                done = True
            else:
                reward, done = 0, False
            transition = trajectories[player][i:i + 3].copy()
            transition.insert(2, reward)
            transition.append(done)

            new_trajectories[player].append(transition)
    return new_trajectories


def set_global_seed(seed: int) -> None:
    """
    Set the global see for reproducing results
    :param seed: (int): The seed
    Note: If using other modules with randomness, they also need to be seeded
    """
    if seed is not None:
        # We only require Tensorflow or PyTorch, not both
        try:
            import tensorflow as tf
            tf.compat.v1.set_random_seed(seed)
        except:
            pass
        try:
            import torch
            torch.manual_seed(seed)
        except:
            pass
        np.random.seed(seed)
        random.seed(seed)


def remove_illegal(action_probs: np.ndarray, legal_actions: List[int]) -> np.ndarray:
    """
    Remove illegal actions and normalize the
        probability vector
    :param action_probs: (numpy.array): A 1 dimention numpy array.
    :param legal_actions: (list): A list of indices of legal actions.
    :return: (numpy.array): A normalized vector without legal actions.
    """
    probs = np.zeros(action_probs.shape[0])
    probs[legal_actions] = action_probs[legal_actions]
    if np.sum(probs) == 0:
        probs[legal_actions] = 1 / len(legal_actions)
    else:
        probs /= sum(probs)
    return probs


def time_difference_good_format(t1: float, t2: float) -> str:
    """
    From two seconds time, compute the difference and give a relevant string of that time delta
    :param t1: first time
    :param t2: second time, higher than first
    :return: string with 'hours', 'minutes', 'secondes'
    """
    delta_t = int(t2 - t1)
    if delta_t < 60:
        if delta_t <= 1:
            return '{} second'.format(delta_t)
        else:
            return '{} seconds'.format(delta_t)
    elif delta_t < 3600:
        minutes = int(delta_t / 60)
        sec = delta_t % 60
        if minutes <= 1:
            if sec <= 1:
                return '{} minute and {} second'.format(minutes, sec)
            else:
                return '{} minute and {} seconds'.format(minutes, sec)
        else:
            if sec <= 1:
                return '{} minutes and {} second'.format(minutes, sec)
            else:
                return '{} minutes and {} seconds'.format(minutes, sec)
    elif delta_t < 3600 * 24:
        hours = int(delta_t / 3600)
        if hours <= 1:
            hours_s = ''
        else:
            hours_s = 's'
        minutes = int((delta_t % 3600) / 60)
        if minutes <= 1:
            minutes_s = ''
        else:
            minutes_s = 's'
        sec = delta_t % 60
        if sec <= 1:
            sec_s = ''
        else:
            sec_s = 's'
        return '{} hour{}, {} minute{} and {} second{}'.format(hours, hours_s, minutes, minutes_s, sec, sec_s)
    else:
        days = int(delta_t / 3600 * 24)
        if days <= 1:
            days_s = ''
        else:
            days_s = 's'
        hours = int((delta_t % (3600 * 24)) / 3600)
        if hours <=1 :
            hours_s = ''
        else:
            hours_s = 's'
        minutes = int((delta_t % 3600) / 60)
        if minutes <= 1:
            minutes_s = ''
        else:
            minutes_s = 's'
        return '{} day{}, {} hour{} and {} minute{}'.format(days, days_s, hours, hours_s, minutes, minutes_s)
