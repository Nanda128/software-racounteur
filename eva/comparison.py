"""Comparing EVA activity between two countries. Built on the analysis functions; no I/O."""
import math
from dataclasses import dataclass

from eva import analysis
from eva.errors import InvalidQueryError


@dataclass(frozen=True)
class CountrySummary:
    """EVA statistics for one country over the compared period.

    Attributes:
        country (str): Country name.
        eva_count (int): Number of EVAs in the period.
        total_hours (float): Total EVA duration in hours (0 if there were none).
        average_hours (float | None): Mean EVA duration in hours, or None if there were no EVAs.
    """
    country: str
    eva_count: int
    total_hours: float
    average_hours: float | None


@dataclass(frozen=True)
class ComparisonResult:
    """Outcome of comparing two countries over an inclusive range of years.

    Attributes:
        start_year (int): First year compared.
        end_year (int): Last year compared.
        summary_a (CountrySummary): Statistics for the first country.
        summary_b (CountrySummary): Statistics for the second country.
        leader (str | None): Country with the greater total duration, or None for a tie.
    """
    start_year: int
    end_year: int
    summary_a: CountrySummary
    summary_b: CountrySummary
    leader: str | None


def summarise_country(records, country, start_year, end_year):
    """Summarises one country's EVAs in an inclusive year range.

    Args:
        records (list[EvaRecord]): All prepared records.
        country (str): Country to summarise.
        start_year (int): First year, inclusive.
        end_year (int): Last year, inclusive.

    Returns:
        CountrySummary: Count, total and average duration (average is None when there are no EVAs).
    """
    selected = analysis.filter_records(records, country, start_year, end_year)
    _, cumulative_hours = analysis.cumulative_duration(selected)

    eva_count = len(selected)
    total_hours = cumulative_hours[-1] if cumulative_hours else 0
    average_hours = total_hours / eva_count if eva_count else None
    return CountrySummary(country, eva_count, total_hours, average_hours)


def compare_countries(records, country_a, country_b, start_year, end_year):
    """Compares two countries' EVA activity between two years, inclusive.

    Args:
        records (list[EvaRecord]): All prepared records.
        country_a (str): First country.
        country_b (str): Second country.
        start_year (int): First year of the period, inclusive.
        end_year (int): Last year of the period, inclusive.

    Returns:
        ComparisonResult: Both summaries and which country has the greater total duration
        (None if the totals are equal).

    Raises:
        InvalidQueryError: If the year range is reversed or a country is not in the data.
    """
    analysis.check_year_range(start_year, end_year)

    known = analysis.known_countries(records)
    unknown = [country for country in (country_a, country_b) if country not in known]
    if unknown:
        raise InvalidQueryError(
            f"unknown country: {', '.join(repr(c) for c in unknown)} "
            f"(known countries: {', '.join(sorted(known))})"
        )

    summary_a = summarise_country(records, country_a, start_year, end_year)
    summary_b = summarise_country(records, country_b, start_year, end_year)
    return ComparisonResult(
        start_year, end_year, summary_a, summary_b, _leader(summary_a, summary_b)
    )


def _leader(summary_a, summary_b):
    """Returns the country with the greater total duration, or None if they are tied."""
    if math.isclose(summary_a.total_hours, summary_b.total_hours, abs_tol=1e-9):
        return None
    return summary_a.country if summary_a.total_hours > summary_b.total_hours else summary_b.country
