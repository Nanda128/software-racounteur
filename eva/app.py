"""Coordinates the application: wires the modules together, adds no logic of its own."""
from eva import analysis, comparison, data_source, presentation, preparation, user_input
from eva.errors import InvalidQueryError

DATA_FILE = "eva-data.json"


def main(argv=None):
    """Loads the data, then runs the cumulative analysis or, with --compare, the country comparison."""
    args = user_input.parse_arguments(argv)
    records = preparation.prepare_records(data_source.load_raw_records(DATA_FILE))

    if args.compare:
        run_country_comparison(records)
    else:
        run_cumulative_analysis(records)


def run_cumulative_analysis(records):
    """Asks the user what to show, then analyses and presents it."""
    try:
        typed_country, start_year, end_year = user_input.prompt_query()
        analysis.check_year_range(start_year, end_year)
    except InvalidQueryError as error:
        print(f"Cannot analyse: {error}")
        return

    country = analysis.resolve_country(typed_country, analysis.known_countries(records))
    selected = analysis.filter_records(records, country, start_year, end_year)
    if not selected:
        print("No EVAs match that country and period.")
        return

    x, y = analysis.cumulative_duration(selected)
    occurances = analysis.count_duration_categories(selected)

    presentation.plot_cumulative_duration(country, x, y)
    print(presentation.format_category_summary(occurances, analysis.category_percentages(occurances)))


def run_country_comparison(records):
    """Asks the user for two countries and a period, then compares and presents them."""
    try:
        country_a, country_b, start_year, end_year = user_input.prompt_comparison_query()
        result = comparison.compare_countries(records, country_a, country_b, start_year, end_year)
    except InvalidQueryError as error:
        print(f"Cannot compare: {error}")
        return

    print(presentation.format_comparison(result))
