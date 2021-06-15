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
            self.test_rules: dict = yaml.load(rules_file, Loader=yaml.SafeLoader)

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

    # def test_rules_engine(self) -> None:
    #     # Complete Test
    #     self.assertDictEqual(
    #         self.R.run(raw_data=self.input_raw, rules_config=self.test_rules),
    #         self.rag_config
    #     )


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
