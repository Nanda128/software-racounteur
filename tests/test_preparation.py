"""Tests for validating raw entries and converting them to EvaRecords."""
import unittest
from datetime import datetime

from eva.models import EvaRecord
from eva.preparation import prepare_records


class PrepareRecordsTests(unittest.TestCase):
    def test_converts_date_and_duration(self):
        raw = [{"country": "USA", "date": "1965-06-03T00:00:00.000", "duration": "1:30"}]
        self.assertEqual(
            prepare_records(raw),
            [EvaRecord(datetime(1965, 6, 3), 1.5, "USA")],
        )

    def test_entries_missing_date_duration_or_country_are_dropped(self):
        raw = [
            {"country": "USA", "duration": "1:00"},
            {"country": "USA", "date": "1965-06-03T00:00:00.000"},
            {"date": "1965-06-03T00:00:00.000", "duration": "1:00"},
            {"country": "Russia", "date": "1966-01-01T00:00:00.000", "duration": "0:30"},
        ]
        self.assertEqual(
            prepare_records(raw),
            [EvaRecord(datetime(1966, 1, 1), 0.5, "Russia")],
        )

    def test_records_are_sorted_by_date(self):
        raw = [
            {"country": "USA", "date": "1970-01-01T00:00:00.000", "duration": "1:00"},
            {"country": "USA", "date": "1965-01-01T00:00:00.000", "duration": "1:00"},
        ]
        self.assertEqual([r.date.year for r in prepare_records(raw)], [1965, 1970])

    def test_empty_input(self):
        self.assertEqual(prepare_records([]), [])


if __name__ == "__main__":
    unittest.main()
