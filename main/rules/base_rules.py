from typing import Callable
import itertools
import logging

"""
Add base rules here! If they're in this file, it'll be autoloaded into RulesEngine.

100% this is not scalable but nice to have initially before doing a proper file pattern per rule
"""


# Text Contains
# data:
#     - raw_text
# variables:
#     - match_case
#     - target


def text_contains(data: str, variables: dict = {}, secrets: dict = {}) -> bool:
    text: str = (
        data["raw_data"] if variables["match_case"] else data["raw_data"].lower()
    )
    logging.debug(f"main.rules.base_rules.text_contains.text: {text}")
    return variables["target"] in text


eq = equal = lambda data, variables, secrets={}: data["value"] == variables["target"]
lt = less_than = lambda data, variables, secrets={}: data["value"] < variables["target"]
gt = greater_than = not lt

is_true = lambda data, variables={}, secrets={}: list(itertools.chain(*[data["value"]]))
