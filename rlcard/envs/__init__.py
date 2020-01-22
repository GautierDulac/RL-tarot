""" Register new environments
"""

from rlcard.envs.registration import register, make

register(
    env_id='tarot',
    entry_point='rlcard.envs.tarot:TarotEnv',
)
