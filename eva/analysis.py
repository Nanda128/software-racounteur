"""Calculations over EVA records. Pure functions: no file, input or display code."""
from eva.errors import InvalidQueryError

EVA_DURATION_CATEGORIES = {0: "short", 1: "standard", 2: "long"}


def known_countries(records):
    """Returns the set of countries present in the records.

    Args:
        records (list[EvaRecord]): Records to inspect.
    """
    return {record.country for record in records}


def resolve_country(typed_country, known):
    """Decides which country a typed name selects.

    Args:
        typed_country (str): Name as typed by the user.
        known (set[str]): Countries present in the data.

    Returns:
        str: The country if it is known, otherwise None, meaning all countries.
    """
    return typed_country if typed_country in known else None


def check_year_range(start_year, end_year):
    """Checks that a year range is not reversed. A missing bound (None) is always fine.

    Raises:
        InvalidQueryError: If start_year is after end_year.
    """
    if start_year is not None and end_year is not None and start_year > end_year:
        raise InvalidQueryError(f"start year {start_year} is after end year {end_year}")


def filter_records(records, country=None, start_year=None, end_year=None):
    """Selects records by country and inclusive year range.

    Args:
        records (list[EvaRecord]): Records to filter.
        country (str, optional): Only keep this country. None keeps all. Defaults to None.
        start_year (int, optional): Lower bound year, inclusive. None means no bound.
        end_year (int, optional): Upper bound year, inclusive. None means no bound.

    Returns:
        list[EvaRecord]: Matching records in their original order.
    """
    return [
        record for record in records
        if (start_year is None or record.date.year >= start_year)
        and (end_year is None or record.date.year <= end_year)
        and (country is None or record.country == country)
    ]


def cumulative_duration(records):
    """Builds the running total of EVA hours.

    Args:
        records (list[EvaRecord]): Records in date order.

    Returns:
        dates (list[datetime]): Date of each EVA
        cumulative_hours (list[float]): Total hours up to and including each EVA
    """
    dates = []
    cumulative_hours = []
    total_hours = 0

    for record in records:
        total_hours += record.duration_hours
        dates.append(record.date)
        cumulative_hours.append(total_hours)

    return dates, cumulative_hours


def categorise_duration(duration_hours):
    """Categorise duration hours based on durations.

    Args:
        duration_hours (float): Amount of hours spent on an EVA event

    Returns:
        str: "short" (under 4 hours), "standard" (4 to under 7) or "long" (7 or more).
    """
    if duration_hours < 4:
        return EVA_DURATION_CATEGORIES[0]
    elif duration_hours < 7:
        return EVA_DURATION_CATEGORIES[1]
    else:
        return EVA_DURATION_CATEGORIES[2]


def count_duration_categories(records):
    """Counts how many EVAs fall in each duration category.

    Args:
        records (list[EvaRecord]): Records to categorise.

    Returns:
        dict[str, int]: Every category mapped to its count (zero if none).
    """
    occurances = {category: 0 for category in EVA_DURATION_CATEGORIES.values()}
    for record in records:
        occurances[categorise_duration(record.duration_hours)] += 1
    return occurances


def category_percentages(occurances):
    """Convert occurances into percentages of the total.

    Args:
        occurances (dict[str, int]): Categories and how many times they occurred.

    Returns:
        dict[str, float]: Each category's share of all EVAs, in percent (all 0.0 if there are none).
    """
    total_evas = sum(occurances.values())
    if total_evas == 0:
        return {cat: 0.0 for cat in occurances}
    return {cat: (occ / total_evas) * 100 for cat, occ in occurances.items()}
