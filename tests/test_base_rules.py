from main.rules import base_rules
import unittest
import pathlib
import logging


class TestBaseRules(unittest.TestCase):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.maxDiff = None

        self.test_resource_path: str = (
            f"{pathlib.Path(__file__).parent.absolute()}/resources"
        )

    def test_text_contains_sunny(self) -> None:
        # Sunny side match case
        self.assertTrue(
            base_rules.text_contains(
                data={"raw_data": " Hello my name is"},
                variables={"match_case": True, "target": "Hello"},
            )
        )

    def test_text_contains_fail(self) -> None:
        self.assertFalse(
            base_rules.text_contains(
                data={"raw_data": " Hello my name is"},
                variables={"match_case": True, "target": "hell"},
            )
        )

    def test_text_contains_match_case_sunny(self) -> None:
        # Sunny side match case
        self.assertTrue(
            base_rules.text_contains(
                data={"raw_data": " Hello my name is"},
                variables={"match_case": False, "target": "hell"},
            )
        )

    def test_text_contains_match_case_fail(self) -> None:
        self.assertFalse(
            base_rules.text_contains(
                data={"raw_data": " Hello my name is"},
                variables={"match_case": True, "target": "hell"},
            )
        )

    def test_equal(self) -> None:
        self.assertTrue(base_rules.eq({"value": 3}, {"target": 3}))

    def test_is_true(self) -> None:
        self.assertTrue(base_rules.is_true({"value": [True, True]}))


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
