""" Register rule-based models or pre-trianed models
"""

from rlcard.models.registration import register, load

register(
    model_id='tarot-rule-v1',
    entry_point='rlcard.models.tarot_rule_models:TAROTRuleModelV1')

register(
    model_id='tarot-bid-rule-v1',
    entry_point='rlcard.models.tarot_bid_rule_models:TAROTBIDRuleModelV1')

register(
    model_id='tarot-dog-rule-v1',
    entry_point='rlcard.models.tarot_dog_rule_models:TAROTDOGRuleModelV1')
