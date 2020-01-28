import random

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
            tf.set_random_seed(seed)
        except:
            pass
        try:
            import torch
            torch.manual_seed(seed)
        except:
            pass
        np.random.seed(seed)
        random.seed(seed)


def remove_illegal(action_probs, legal_actions):
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
