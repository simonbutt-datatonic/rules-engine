from main.rules.base_rules import text_contains
from main.rules_engine import RulesEngine
from unittest.mock import patch
import pytest
import unittest
import pathlib
import json
import yaml
import logging


class TestRulesEngine(unittest.TestCase):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.maxDiff = None

        test_resource_path: str = (
            f"{pathlib.Path(__file__).parent.absolute()}/resources"
        )

        with open(f"{test_resource_path}/test_rules_engine_correct.json") as rag_file:
            self.rag_config: dict = json.load(rag_file)

        with open(f"{test_resource_path}/test_rules_input_raw.json") as raw_file:
            self.input_raw: dict = json.load(raw_file)

        with open(f"{test_resource_path}/test_rules_config.yml") as rules_file:
            self.rules_config: dict = yaml.load(rules_file, Loader=yaml.SafeLoader)

        # Everything is stateless, so this is less bad than it seems
        self.R = RulesEngine()

    def test_pull_external_operators(self) -> None:
        self.assertDictEqual(self.R._pull_external_operators([]), {})

    def test_pull_operators_sunny(self) -> None:
        self.assertDictEqual(
            self.R._pull_operators(["text_contains"]), {"text_contains": text_contains}
        )

    def test_pull_operators_fail(self) -> None:
        with pytest.raises(Exception) as exec_info:
            self.R._pull_operators(["text_contains", "does_not_exist"]),

        self.assertTrue("does_not_exist" in str(exec_info.value))

    def test_formulate_secrets(self) -> None:
        # TODO: stub
        self.assertDictEqual(self.R._formulate_secrets(required_secrets={}), {})

    def test_traverse_data(self) -> None:
        with pytest.raises(KeyError) as exec_info:
            self.R._traverse_data({"a.b": 2}, "b"),

        self.assertTrue("b" in str(exec_info.value))

    def test_formulate_data(self) -> None:
        self.assertEqual(
            self.R._formulate_data(
                raw_data=self.input_raw,
                input_data_config=self.rules_config["output_schema"]["y_1"][
                    "input_data"
                ],
            ),
            {"raw_data": "Hello my name is Simon. How are you?"},
        )

    def test_run_sunny(self) -> None:
        # TODO: Complete Test
        self.assertDictEqual(
            self.R.run(raw_data=self.input_raw, rules_config=self.rules_config),
            self.rag_config,
        )


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
