from main.rules.base_rules import text_contains
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
            text_contains(
                raw_text=" Hello my name is",
                target="Hello",
            )
        )

    def test_text_contains_fail(self) -> None:
        self.assertFalse(
            text_contains(
                raw_text=" Hello my name is",
                target="hell",
            )
        )

    def test_text_contains_match_case_sunny(self) -> None:
        # Sunny side match case
        self.assertTrue(
            text_contains(raw_text=" Hello my name is", target="hell", match_case=False)
        )

    def test_text_contains_match_case_fail(self) -> None:
        self.assertFalse(
            text_contains(raw_text=" Hello my name is", target="hell", match_case=True)
        )


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
