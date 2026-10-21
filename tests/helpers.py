"""Shared test helpers."""
from datetime import datetime

from eva.models import EvaRecord


def eva(country, year, hours, month=1, day=1):
    """Builds an EvaRecord with the given country, date and duration in hours."""
    return EvaRecord(datetime(year, month, day), hours, country)
