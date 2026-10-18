"""Prompting the user and interpreting what they type."""
import argparse

from eva.errors import InvalidQueryError


def prompt_query():
    """Handles input from user for program's operation.

    Returns:
        country (str): Country name as typed (blank if none was entered)
        start_year (int): Lower bound year of data to show, or None for no bound
        end_year (int): Upper bound year of data to show, or None for no bound

    Raises:
        InvalidQueryError: If a year is entered but is not a whole number.
    """
    country = input("Enter country (Or nothing for all countries):").strip()
    start_year = _parse_optional_year(input("Data start year: "), "start year")
    end_year = _parse_optional_year(input("Data end year: "), "end year")
    return country, start_year, end_year


def parse_arguments(argv=None):
    """Reads command-line options.

    Args:
        argv (list[str], optional): Arguments to parse. Defaults to sys.argv[1:].

    Returns:
        argparse.Namespace: With `compare` True if the country comparison was requested.
    """
    parser = argparse.ArgumentParser(description="Analyse extravehicular activity (EVA) data.")
    parser.add_argument(
        "--compare", action="store_true",
        help="compare EVA activity between two countries instead of plotting cumulative duration",
    )
    return parser.parse_args(argv)


def prompt_comparison_query():
    """Asks the user for the two countries and the year range to compare.

    Returns:
        country_a (str): First country name as typed
        country_b (str): Second country name as typed
        start_year (int): First year of the period
        end_year (int): Last year of the period

    Raises:
        InvalidQueryError: If a year is missing or is not a whole number.
    """
    country_a = input("Country A: ").strip()
    country_b = input("Country B: ").strip()
    start_year = _require_year(input("Start year: "), "start year")
    end_year = _require_year(input("End year: "), "end year")
    return country_a, country_b, start_year, end_year


def _require_year(text, label):
    """Converts typed text to a year, raising InvalidQueryError if it is blank or not a number."""
    try:
        return int(text.strip())
    except ValueError:
        raise InvalidQueryError(f"{label} must be a whole number, got {text.strip()!r}") from None


def _parse_optional_year(text, label):
    """Converts typed text to a year; blank text means no bound (None)."""
    return _require_year(text, label) if text.strip() else None
