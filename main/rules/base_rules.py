from typing import Callable

"""
Add base rules here! If they're in this file, it'll be autoloaded into RulesEngine.

100% this is not scalable but nice to have initially before doing a proper file pattern per rule
"""


def text_contains(raw_text: str, target: str, match_case: bool = True) -> bool:
    text: str = raw_text if match_case else raw_text.lower()

    return target in text
