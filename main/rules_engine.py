from main.rules import base_rules as base
from inspect import getmembers, isfunction
import yaml
import logging
from typing import List

"""
    Goals:
        -   To be better than SQL for deeply nested data
        -   To offer logic on temporary abstractions without large latency overhead

    Basic Rules Engine API designed to be part of an event driven solution architecture.
    This API will configurable to both:
        -   http
        -   pubsub

    This is designed for NoSQL data but will be configurable to multiple backends

    Input:
        raw_data: dict


"""


class RulesEngine:
    def __init__(self) -> None:
        self.log_path: str = "main.rules_engine"

    def _pull_external_operators(self, operator_id_list: List[str]) -> dict:
        # Mocking for the time being
        return {}

    def _pull_operators(self, operator_id_list: List[str]) -> dict:
        # Add option for external operators

        logging.debug(
            f"{self.log_path}._get_rules_operator_config.operator_id_list: {operator_id_list}"
        )

        base_modules_config: List[str] = {
            key: value for (key, value) in getmembers(base, isfunction)
        }

        logging.debug(
            f"{self.log_path}._get_rules_operator_config.base_modules : {list(base_modules_config.keys())}"
        )

        external_modules_config: dict = self._pull_external_operators(operator_id_list)

        intersection: set = set(operator_id_list) - set(base_modules_config)

        # False if Set empty
        if not bool(intersection):

            return {**base_modules_config, **external_modules_config}
        else:
            raise Exception(
                f"{self.log_path}._get_rules_operator_config - Operators not found: {intersection}"
            )

    # def run(self, raw_data: dict, rules_config: dict) -> dict:

    #     result_config: dict = {}

    #     # ROC --> rules orchestration config
    #     ROC: dict = rules_config.pop("output_schema")
    #     lambda_rules_config: dict = self._pull_operators(
    #         operator_id_list=[ROC[key]["rule_id"] for key in ROC.keys()]
    #     )

    #     for output_key in ROC.keys():
    #         logging.debug(f"{self.log_path}.rules_engine.ROC.output_key: {output_key}")

    #     return result_config
