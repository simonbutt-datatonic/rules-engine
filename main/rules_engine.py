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
            key: value
            for (key, value) in getmembers(base, isfunction)
            if key in operator_id_list
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

    def _traverse_data(self, data: dict, value: str):
        key_list: list = value.split(".")

        # TODO: make this less hacky. Recursion would avoid this mess
        _data_tmp = data
        for key in key_list:
            try:
                _data_tmp_new = _data_tmp.copy()[key]
            except KeyError:
                logging.error(
                    f"{self.log_path}/_traverse_data.value: Data source not found: {value}"
                )
                raise KeyError(value)
            _data_tmp = _data_tmp_new
        return _data_tmp

    def _formulate_data(self, raw_data: dict, input_data_config: dict):

        # TODO: Both _formulate_data & _traverse_data are low hanging tech debt fruit

        return {
            key: [
                self._traverse_data(raw_data, value) for value in input_data_config[key]
            ]
            if key.endswith("_list")
            else self._traverse_data(raw_data, input_data_config[key])
            for key in input_data_config
        }

    def _formulate_secrets(self, required_secrets: dict) -> dict:
        # TODO: hook up to a secrets manager

        return {}

    def _execute_rules(self, raw_data: dict, schema: dict, operator: dict):

        data = self._formulate_data(raw_data, schema["input_data"])

        # TODO: Figure out if we want to split this out a la kubernetes variables
        return operator(
            data,
            variables=schema.get("required_variables", {}),
            secrets=schema.get("required_secrets", {}),
        )

    def run(self, raw_data: dict, rules_config: dict) -> dict:

        """
        Key (in the meantime)
        result_config: output
        schema_config: everything in your `rules_config.output_schema`
        operator_config: all the operators used to build `result_config`
        """

        schema_config: dict = rules_config.pop("output_schema")
        operator_config: dict = self._pull_operators(
            operator_id_list=[
                schema_config[key]["rule_id"] for key in schema_config.keys()
            ]
        )

        return {
            output_key: self._execute_rules(
                raw_data=raw_data,
                schema=schema_config[output_key],
                operator=operator_config[schema_config[output_key]["rule_id"]],
            )
            for output_key in schema_config.keys()
        }
