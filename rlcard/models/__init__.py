""" Register rule-based models or pre-trianed models
"""

from rlcard.models.registration import register, load

register(
    model_id='tarot-rule-v1',
    entry_point='rlcard.models.tarot_rule_models:TAROTRuleModelV1')

