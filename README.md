# software-racounteur

A command-line tool for exploring EVA (spacewalk) data in `eva-data.json`. It
plots cumulative EVA time, sorts EVAs into short, standard and long, and
compares two countries over a period.

## Set up

You need Python 3.10 or newer. Run everything from the repository root, since
the data file is read from the current directory.

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate    macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
```

## Run

**Cumulative duration and categories**

```bash
python evacodev2.py
```

Enter a country (blank means all), a start year and an end year (blank means no
limit). It saves `cumulative_duration_<country>.png`, shows the plot, then
prints how many EVAs were short (under 4 h), standard (4 to under 7 h) and long
(7 h or more), with percentages. If nothing matches, it says so instead of
plotting.

**Compare two countries**

```bash
python evacodev2.py --compare
```

Enter Country A, Country B, a start year and an end year (both included). For
each country you get the number of EVAs, total hours and average hours, then
which has more total time, or a tie. A country with no EVAs shows zeros and an
average of "unavailable". Unknown countries and bad years print a message
instead of crashing. Names are case-sensitive (`USA`, `Russia`).

## Test

```bash
python -m unittest -v
```

Standard library only. Run it from the repository root, because some tests read
the real data file.

## How the code is organised

`evacodev2.py` just starts the app. The work is in `eva/`, one module per job:

| Module | Job |
| --- | --- |
| `app.py` | Runs the program and wires the other modules together |
| `data_source.py` | Reads the JSON file |
| `preparation.py` | Cleans entries and converts dates and durations |
| `models.py` | The `EvaRecord` type |
| `analysis.py` | Calculations: filtering, running totals, categories, percentages |
| `comparison.py` | The two-country comparison |
| `presentation.py` | The plot and text output |
| `user_input.py` | Prompts, the `--compare` flag, parsing typed input |
| `errors.py` | `InvalidQueryError` for requests that can't be answered |

`app` uses all the others, and `comparison` uses `analysis`. The calculation
modules never read files or print.

## More documentation

- [docs/architectural-assessment.md](docs/architectural-assessment.md): what the inherited code did and what was wrong with it
- [docs/architecture.md](docs/architecture.md): the module structure, diagram and interfaces
- [docs/adr/](docs/adr/): the two architectural decisions
- [docs/evaluation.md](docs/evaluation.md): test evidence and a before/after comparison

## Good to know

- Bad input (a reversed range, a year that isn't a number, no matching EVAs)
  prints a message in both modes. In the first mode an unknown country quietly
  means "all countries"; `--compare` rejects it.
- Plot images are written to the current directory and git-ignored.
- More caveats are in `docs/evaluation.md`.
