"""Tests for the country comparison (new FR). Pure data in, results out: no files or prompts."""
import unittest

from eva.comparison import compare_countries
from eva.errors import InvalidQueryError
from tests.helpers import eva


class CompareCountriesTests(unittest.TestCase):
    def __init__(self):
        self.records = None

    def setUp(self):
        self.records = [
            eva("USA", 1964, 9.0, 12, 31),     # before the period
            eva("USA", 1965, 2.0, 1, 1),       # first day of start year: included
            eva("Russia", 1965, 1.0, 6, 1),
            eva("Russia", 1966, 2.0, 1, 1),
            eva("Russia", 1966, 1.0, 6, 1),
            eva("USA", 1966, 4.0, 12, 31),     # last day of end year: included
            eva("USA", 1967, 10.0, 1, 1),      # after the period
        ]

    def test_counts_totals_and_averages_for_each_country(self):
        result = compare_countries(self.records, "USA", "Russia", 1965, 1966)

        self.assertEqual(result.summary_a.country, "USA")
        self.assertEqual(result.summary_a.eva_count, 2)
        self.assertAlmostEqual(result.summary_a.total_hours, 6.0)
        self.assertAlmostEqual(result.summary_a.average_hours, 3.0)

        self.assertEqual(result.summary_b.country, "Russia")
        self.assertEqual(result.summary_b.eva_count, 3)
        self.assertAlmostEqual(result.summary_b.total_hours, 4.0)
        self.assertAlmostEqual(result.summary_b.average_hours, 4.0 / 3)

    def test_country_with_greater_total_duration_is_the_leader(self):
        result = compare_countries(self.records, "USA", "Russia", 1965, 1966)
        self.assertEqual(result.leader, "USA")

    def test_leader_does_not_depend_on_argument_order(self):
        result = compare_countries(self.records, "Russia", "USA", 1965, 1966)
        self.assertEqual(result.leader, "USA")

    def test_start_and_end_years_are_both_included(self):
        result = compare_countries(self.records, "USA", "Russia", 1965, 1965)
        self.assertEqual(result.summary_a.eva_count, 1)
        self.assertAlmostEqual(result.summary_a.total_hours, 2.0)

        result = compare_countries(self.records, "USA", "Russia", 1966, 1966)
        self.assertEqual(result.summary_a.eva_count, 1)
        self.assertAlmostEqual(result.summary_a.total_hours, 4.0)

    def test_country_without_matching_evas_has_zero_totals_and_unavailable_average(self):
        result = compare_countries(self.records, "USA", "Russia", 1967, 1967)

        self.assertEqual(result.summary_b.eva_count, 0)
        self.assertEqual(result.summary_b.total_hours, 0)
        self.assertIsNone(result.summary_b.average_hours)
        self.assertEqual(result.leader, "USA")

    def test_equal_totals_are_reported_as_a_tie(self):
        records = [eva("USA", 1970, 3.0), eva("Russia", 1970, 1.0), eva("Russia", 1970, 2.0)]
        result = compare_countries(records, "USA", "Russia", 1970, 1970)
        self.assertIsNone(result.leader)

    def test_tie_is_detected_despite_floating_point_rounding(self):
        # 0.1 + 0.2 != 0.3 exactly in floating point, but the totals are equal as durations.
        records = [eva("USA", 1970, 0.3), eva("Russia", 1970, 0.1), eva("Russia", 1970, 0.2)]
        result = compare_countries(records, "USA", "Russia", 1970, 1970)
        self.assertIsNone(result.leader)

    def test_no_matching_evas_for_either_country_is_a_tie_at_zero(self):
        result = compare_countries(self.records, "USA", "Russia", 2000, 2001)
        self.assertEqual(result.summary_a.eva_count, 0)
        self.assertEqual(result.summary_b.eva_count, 0)
        self.assertIsNone(result.leader)


class CompareCountriesInvalidInputTests(unittest.TestCase):
    def __init__(self):
        self.records = None

    def setUp(self):
        self.records = [eva("USA", 1965, 2.0), eva("Russia", 1965, 1.0)]

    def test_start_year_after_end_year_is_rejected(self):
        with self.assertRaises(InvalidQueryError):
            compare_countries(self.records, "USA", "Russia", 1975, 1965)

    def test_unknown_country_is_rejected_and_named(self):
        with self.assertRaises(InvalidQueryError) as context:
            compare_countries(self.records, "USA", "Narnia", 1965, 1975)
        self.assertIn("Narnia", str(context.exception))

    def test_all_unknown_countries_are_named(self):
        with self.assertRaises(InvalidQueryError) as context:
            compare_countries(self.records, "Narnia", "Oz", 1965, 1975)
        self.assertIn("Narnia", str(context.exception))
        self.assertIn("Oz", str(context.exception))

    def test_invalid_query_error_is_a_value_error(self):
        self.assertTrue(issubclass(InvalidQueryError, ValueError))


if __name__ == "__main__":
    unittest.main()
