"""Tests for the existing analysis operations, run on small hand-written data."""
import unittest

from eva import analysis
from eva.errors import InvalidQueryError
from tests.helpers import eva


class CategoriseDurationTests(unittest.TestCase):
    def test_category_boundaries(self):
        cases = [
            (0, "short"), (3.99, "short"),
            (4, "standard"), (6.99, "standard"),
            (7, "long"), (12.5, "long"),
        ]
        for hours, expected in cases:
            with self.subTest(hours=hours):
                self.assertEqual(analysis.categorise_duration(hours), expected)


class CountDurationCategoriesTests(unittest.TestCase):
    def test_counts_each_category(self):
        records = [eva("USA", 1970, h) for h in (1, 3.5, 4, 5, 6.5, 7, 8)]
        self.assertEqual(
            analysis.count_duration_categories(records),
            {"short": 2, "standard": 3, "long": 2},
        )

    def test_empty_input_gives_zero_for_every_category(self):
        self.assertEqual(
            analysis.count_duration_categories([]),
            {"short": 0, "standard": 0, "long": 0},
        )


class CategoryPercentagesTests(unittest.TestCase):
    def test_percentages_of_total(self):
        self.assertEqual(
            analysis.category_percentages({"short": 1, "standard": 1, "long": 2}),
            {"short": 25.0, "standard": 25.0, "long": 50.0},
        )


    def test_no_evas_gives_zero_percentages_instead_of_dividing_by_zero(self):
        self.assertEqual(
            analysis.category_percentages({"short": 0, "standard": 0, "long": 0}),
            {"short": 0.0, "standard": 0.0, "long": 0.0},
        )


class ResolveCountryTests(unittest.TestCase):
    def test_known_country_is_selected(self):
        self.assertEqual(analysis.resolve_country("USA", {"USA", "Russia"}), "USA")

    def test_unknown_or_blank_country_means_all_countries(self):
        self.assertIsNone(analysis.resolve_country("Narnia", {"USA", "Russia"}))
        self.assertIsNone(analysis.resolve_country("", {"USA", "Russia"}))


class CheckYearRangeTests(unittest.TestCase):
    def test_reversed_range_is_rejected(self):
        with self.assertRaises(InvalidQueryError):
            analysis.check_year_range(1975, 1965)

    def test_equal_ordered_and_open_ranges_are_accepted(self):
        for start, end in [(1965, 1965), (1965, 1975), (None, 1975), (1965, None), (None, None)]:
            with self.subTest(start=start, end=end):
                analysis.check_year_range(start, end)


class FilterRecordsTests(unittest.TestCase):
    def setUp(self):
        self.records = [
            eva("USA", 1965, 1.0), eva("Russia", 1966, 2.0),
            eva("USA", 1967, 3.0), eva("Russia", 1968, 4.0),
        ]

    def test_no_filters_keeps_everything_in_order(self):
        self.assertEqual(analysis.filter_records(self.records), self.records)

    def test_year_bounds_are_inclusive(self):
        selected = analysis.filter_records(self.records, start_year=1966, end_year=1967)
        self.assertEqual([r.date.year for r in selected], [1966, 1967])

    def test_country_filter(self):
        selected = analysis.filter_records(self.records, country="USA")
        self.assertEqual([r.date.year for r in selected], [1965, 1967])

    def test_reversed_year_range_matches_nothing(self):
        self.assertEqual(analysis.filter_records(self.records, start_year=1968, end_year=1965), [])


class CumulativeDurationTests(unittest.TestCase):
    def test_running_total(self):
        records = [eva("USA", 1965, 1.5), eva("USA", 1966, 2.0), eva("USA", 1967, 0.5)]
        dates, cumulative = analysis.cumulative_duration(records)
        self.assertEqual([d.year for d in dates], [1965, 1966, 1967])
        self.assertEqual(cumulative, [1.5, 3.5, 4.0])

    def test_empty_input(self):
        self.assertEqual(analysis.cumulative_duration([]), ([], []))


class KnownCountriesTests(unittest.TestCase):
    def test_distinct_countries(self):
        records = [eva("USA", 1965, 1), eva("USA", 1966, 1), eva("Russia", 1967, 1)]
        self.assertEqual(analysis.known_countries(records), {"USA", "Russia"})


if __name__ == "__main__":
    unittest.main()
