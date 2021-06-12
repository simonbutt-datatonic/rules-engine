from yaml.loader import Loader
from main.rules_engine import rules_engine
import unittest
import pathlib
import json
import yaml


class TestHello(unittest.TestCase):
    def test_rules_engine(self) -> None:

        test_resource_path: str = (
            f"{pathlib.Path(__file__).parent.absolute()}/resources"
        )

        with open(f"{test_resource_path}/test_rules_engine_correct.json") as rag_file:
            rag_config: dict = json.load(rag_file)

        with open(f"{test_resource_path}/test_rules_input_raw.json") as raw_file:
            input_raw: dict = json.load(raw_file)

        with open(f"{test_resource_path}/test_rules_config.yml") as rules_file:
            test_rules: dict = yaml.load(rules_file, Loader=yaml.SafeLoader)

        self.assertDictEqual(
            rag_config, rules_engine(raw_data=input_raw, rules_config=test_rules)
        )


if __name__ == "__main__":
    unittest.main()
