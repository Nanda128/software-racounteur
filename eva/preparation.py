"""Validating raw EVA entries and converting them to typed records."""
from datetime import datetime

from eva.models import EvaRecord


def prepare_records(raw_records):
    """Drops unusable entries and converts the rest to EvaRecords.

    An entry is unusable if it lacks a date, a duration or a country.

    Args:
        raw_records (list[dict]): Entries as returned by the data source.

    Returns:
        list[EvaRecord]: Valid records sorted by date.
    """
    records = []

    for eva in raw_records:
        date_text = eva.get("date")
        duration_text = eva.get("duration")
        country = eva.get("country")

        if not date_text or not duration_text or not country:
            continue

        date = datetime.fromisoformat(date_text)
        hours, minutes = map(int, duration_text.split(":"))
        records.append(EvaRecord(date, hours + minutes / 60, country))

    records.sort(key=lambda record: record.date)
    return records
