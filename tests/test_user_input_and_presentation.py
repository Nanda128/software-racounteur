"""Tests for the thin input-parsing and text-formatting layers around the comparison."""
import unittest
from unittest import mock

from eva.comparison import ComparisonResult, CountrySummary
from eva.errors import InvalidQueryError
from eva.presentation import format_comparison
from eva.user_input import parse_arguments, prompt_comparison_query, prompt_query


def prompt_with(*answers):
    with mock.patch("builtins.input", side_effect=answers):
        return prompt_query()
    return None


class PromptQueryTests(unittest.TestCase):

    def test_returns_typed_country_and_integer_years(self):
        self.assertEqual(prompt_with(" USA ", " 1965 ", "1975"), ("USA", 1965, 1975))

    def test_blank_answers_mean_no_country_and_no_year_bounds(self):
        self.assertEqual(prompt_with("", "", ""), ("", None, None))

    def test_non_numeric_year_is_an_invalid_query(self):
        with self.assertRaises(InvalidQueryError):
            prompt_with("USA", "abc", "")


class PromptComparisonQueryTests(unittest.TestCase):

    def test_returns_trimmed_names_and_integer_years(self):
        self.assertEqual(
            self.prompt_with(" USA ", "Russia", " 1965", "1975 "),
            ("USA", "Russia", 1965, 1975),
        )

    def test_non_numeric_year_is_an_invalid_query(self):
        with self.assertRaises(InvalidQueryError):
            self.prompt_with("USA", "Russia", "abc", "1975")

    def test_blank_year_is_an_invalid_query(self):
        with self.assertRaises(InvalidQueryError):
            self.prompt_with("USA", "Russia", "1965", "")


class ParseArgumentsTests(unittest.TestCase):
    def test_default_is_not_compare(self):
        self.assertFalse(parse_arguments([]).compare)

    def test_compare_flag(self):
        self.assertTrue(parse_arguments(["--compare"]).compare)


def result(summary_b, leader):
    summary_a = CountrySummary("USA", 2, 6.0, 3.0)
    return ComparisonResult(1965, 1966, summary_a, summary_b, leader)


class FormatComparisonTests(unittest.TestCase):

    def test_shows_statistics_and_leader(self):
        text = format_comparison(result(CountrySummary("Russia", 3, 4.0, 4.0 / 3), "USA"))
        self.assertIn("1965 to 1966", text)
        self.assertIn("Total EVAs: 2", text)
        self.assertIn("Total duration (hours): 6.00", text)
        self.assertIn("Average duration (hours): 1.33", text)
        self.assertIn("Result: USA has the greater total EVA duration", text)

    def test_missing_average_is_shown_as_unavailable(self):
        text = format_comparison(result(CountrySummary("Russia", 0, 0, None), "USA"))
        self.assertIn("Average duration (hours): unavailable", text)

    def test_tie_is_reported(self):
        text = format_comparison(result(CountrySummary("Russia", 2, 6.0, 3.0), None))
        self.assertIn("tie", text)


if __name__ == "__main__":
    unittest.main()
