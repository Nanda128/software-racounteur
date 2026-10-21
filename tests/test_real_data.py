"""End-to-end checks on the real data file; pin behaviour recorded before the restructuring (AR5)."""
import unittest
from pathlib import Path

from eva import analysis, data_source, preparation
from eva.comparison import compare_countries

DATA_FILE = Path(__file__).resolve().parent.parent / "eva-data.json"


class RealDataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.records = preparation.prepare_records(data_source.load_raw_records(str(DATA_FILE)))

    def test_usable_record_count(self):
        self.assertEqual(len(self.records), 330)

    def test_duration_categories_for_usa_1965_to_1975_match_original_script(self):
        selected = analysis.filter_records(self.records, "USA", 1965, 1975)
        self.assertEqual(
            analysis.count_duration_categories(selected),
            {"short": 29, "standard": 9, "long": 7},
        )

    def test_duration_categories_for_all_records_match_original_script(self):
        self.assertEqual(
            analysis.count_duration_categories(self.records),
            {"short": 71, "standard": 187, "long": 72},
        )

    def test_comparison_agrees_with_the_data_for_1965_to_1975(self):
        result = compare_countries(self.records, "USA", "Russia", 1965, 1975)
        self.assertEqual(result.summary_a.eva_count, 45)
        self.assertAlmostEqual(result.summary_a.total_hours, 140.48, places=2)
        self.assertEqual(result.summary_b.eva_count, 0)
        self.assertIsNone(result.summary_b.average_hours)
        self.assertEqual(result.leader, "USA")


if __name__ == "__main__":
    unittest.main()
