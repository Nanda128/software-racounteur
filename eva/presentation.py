"""Presenting results: plots and text. Receives plain values, computes nothing."""
import matplotlib.pyplot as plt

ALL_COUNTRIES_LABEL = "all countries"


def plot_cumulative_duration(country, x, y):
    """Plots a given cumulative graph, saves it as a PNG and shows it.

    Args:
        country (str): Name of country being plotted, or None for all countries
        x (list): x data
        y (list): y data
    """
    country_name = country or ALL_COUNTRIES_LABEL
    plt.plot(x, y)
    plt.xlabel("Year")
    plt.ylabel(f"Cumulative EVA duration (hours) {country_name}")
    plt.tight_layout()
    plt.savefig(f"cumulative_duration_{country_name}.png")
    plt.show()


def format_category_summary(occurances, percentages):
    """Formats duration-category counts and percentages as text.

    Args:
        occurances (dict[str, int]): Category counts.
        percentages (dict[str, float]): Category percentages.

    Returns:
        str: Two lines, the counts then the percentages.
    """
    formatted = {cat: str(pct) + "%" for cat, pct in percentages.items()}
    return f"{occurances}\n{formatted}"


def format_comparison(result):
    """Formats a country comparison as text.

    Args:
        result (ComparisonResult): Comparison to present.

    Returns:
        str: A heading, one block of statistics per country and the outcome.
    """
    lines = [f"EVA comparison, {result.start_year} to {result.end_year} (inclusive)"]
    for summary in (result.summary_a, result.summary_b):
        average = "unavailable" if summary.average_hours is None else f"{summary.average_hours:.2f}"
        lines += [
            f"{summary.country}:",
            f"  Total EVAs: {summary.eva_count}",
            f"  Total duration (hours): {summary.total_hours:.2f}",
            f"  Average duration (hours): {average}",
        ]
    if result.leader is None:
        lines.append("Result: tie, both countries have the same total EVA duration")
    else:
        lines.append(f"Result: {result.leader} has the greater total EVA duration")
    return "\n".join(lines)
