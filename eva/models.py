"""Core data type shared by data preparation and analysis."""
from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class EvaRecord:
    """A single extravehicular activity with typed, validated fields.

    Attributes:
        date (datetime): When the EVA took place.
        duration_hours (float): Length of the EVA in decimal hours.
        country (str): Country that performed the EVA.
    """

    date: datetime
    duration_hours: float
    country: str
