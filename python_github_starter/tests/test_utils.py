import unittest

from utils import validate_title


class ValidateTitleTests(unittest.TestCase):
    def test_trims_whitespace(self):
        self.assertEqual(validate_title("  Study Python  "), "Study Python")

    def test_rejects_empty_title(self):
        with self.assertRaises(ValueError):
            validate_title(" ")

    def test_rejects_title_over_120_characters(self):
        with self.assertRaises(ValueError):
            validate_title("x" * 121)

    def test_rejects_non_string(self):
        with self.assertRaises(ValueError):
            validate_title(None)


if __name__ == "__main__":
    unittest.main()
