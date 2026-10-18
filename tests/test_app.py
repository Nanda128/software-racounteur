"""Tests for the coordination layer: bad input is reported, not crashed on, and the plot is skipped."""
import io
import unittest
from contextlib import redirect_stdout
from unittest import mock

from eva import app
from tests.helpers import eva


def run(function, records, *answers):
    """Runs an app workflow with scripted answers; returns (printed text, plot mock)."""
    output = io.StringIO()
    with mock.patch("builtins.input", side_effect=answers), \
            mock.patch("eva.presentation.plot_cumulative_duration") as plot, \
            redirect_stdout(output):
        function(records)
    return output.getvalue(), plot


class CumulativeAnalysisTests(unittest.TestCase):
    def __init__(self):
        self.records = None

    def setUp(self):
        self.records = [eva("USA", 1965, 2.0), eva("USA", 1966, 5.0), eva("Russia", 1966, 8.0)]

    def test_prints_category_counts_and_percentages_and_plots(self):
        text, plot = run(app.run_cumulative_analysis, self.records, "USA", "", "")
        self.assertIn("{'short': 1, 'standard': 1, 'long': 0}", text)
        self.assertIn("50.0%", text)
        plot.assert_called_once()

    def test_unknown_country_means_all_countries(self):
        text, _ = run(app.run_cumulative_analysis, self.records, "Narnia", "", "")
        self.assertIn("{'short': 1, 'standard': 1, 'long': 1}", text)

    def test_reversed_years_are_reported_without_plotting(self):
        text, plot = run(app.run_cumulative_analysis, self.records, "USA", "1975", "1965")
        self.assertIn("Cannot analyse: start year 1975 is after end year 1965", text)
        plot.assert_not_called()

    def test_non_numeric_year_is_reported_without_plotting(self):
        text, plot = run(app.run_cumulative_analysis, self.records, "USA", "abc", "")
        self.assertIn("Cannot analyse", text)
        plot.assert_not_called()

    def test_no_matching_evas_is_reported_without_plotting(self):
        text, plot = run(app.run_cumulative_analysis, self.records, "USA", "2200", "2300")
        self.assertIn("No EVAs match", text)
        plot.assert_not_called()


class CountryComparisonTests(unittest.TestCase):
    def __init__(self):
        self.records = None

    def setUp(self):
        self.records = [eva("USA", 1965, 2.0), eva("Russia", 1965, 1.0)]

    def test_prints_comparison(self):
        text, _ = run(app.run_country_comparison, self.records, "USA", "Russia", "1965", "1965")
        self.assertIn("Result: USA has the greater total EVA duration", text)

    def test_unknown_country_is_reported(self):
        text, _ = run(app.run_country_comparison, self.records, "USA", "Narnia", "1965", "1965")
        self.assertIn("Cannot compare: unknown country: 'Narnia'", text)

    def test_reversed_years_are_reported(self):
        text, _ = run(app.run_country_comparison, self.records, "USA", "Russia", "1975", "1965")
        self.assertIn("Cannot compare: start year 1975 is after end year 1965", text)


if __name__ == "__main__":
    unittest.main()
