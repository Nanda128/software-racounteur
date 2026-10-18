# Evaluation

## Tests

```bash
python -m unittest -v
```

Latest run:

```text
Ran 55 tests in 0.007s

OK
```

Standard library only. Every test uses known inputs and checks exact results.

| File | Checks |
| --- | --- |
| `tests/test_comparison.py` | The new comparison, with hand-worked numbers: counts, totals, averages, both end years included, no matches (zero hours, average unavailable), ties (including float rounding), reversed years, unknown countries |
| `tests/test_analysis.py` | Filtering, running totals, percentages (including none to count), the 4 h / 7 h category boundaries, country selection, year-range check |
| `tests/test_preparation.py` | Incomplete entries dropped, durations converted, records sorted |
| `tests/test_user_input_and_presentation.py` | Both sets of prompts (blank and non-numeric years), the `--compare` flag, text output |
| `tests/test_app.py` | Both modes end to end with scripted input: reversed years, bad years, no matches and unknown countries are reported, and nothing is plotted when there is nothing to plot |
| `tests/test_real_data.py` | Real data: the numbers the original script gave (`USA 1965-1975` is 29/9/7 short/standard/long; all records is 71/187/72), and the comparison against an independent calculation |

**Would they catch a mistake?** I broke the code four ways, one at a time, on a scratch copy: exclusive end year, `>=` instead of `>` on the year check, `0` instead of "unavailable" for an empty average, and a shifted category boundary.
Each one made tests fail.

**Does the old behaviour still work?** Before restructuring, I ran the original script on 12 inputs and recorded the output, exit status and a hash of the saved plot. 
After restructuring, 9 matched exactly. 
The other 3 are inputs that crash the original with `ZeroDivisionError`. 
They still crashed the same way and saved the same plot, but no longer printed the counts line just before  crashing. 
Adding the comparison changed nothing in those 12 results.

Later I made the original mode handle bad input (see [architecture.md](architecture.md#a-later-fix)). 
Now 8 of the 12 are identical and the other 4 are the ones that used to crash: reversed years, non-numeric years, and two empty results. 
They now print a message, exit normally and don't draw an empty plot. 
Every input that worked before still gives the same output and the same plot.

The plot call itself isn't tested (it needs a display); `app.py` is, with the plot call replaced.

## Before and after

Measured with a small script on commit `d3f969b` and on the current code.

| | Before | After |
| --- | --- | --- |
| Source files | 1 | 11 |
| Lines (no blanks or comments) | 98 | 376 |
| Functions | 5 | 24 |
| Longest function | 37 lines | 32 lines (mostly docstring) |
| Statements run on import | 10 | 0 |
| Functions reading shared globals | 2 | 0 |
| Tests | 0 | 55 |
| Features | 1 | 2 |

## Questions from the brief

**How many modules changed to add the new feature?** Five files: two new (`comparison.py`, `errors.py`) and three existing ones with additions (`app.py`, `presentation.py`, `user_input.py`). 
Loading, preparation and
analysis weren't touched. In the old script it would have been edits to the one file that holds everything.

**Which modules depend on which?** `app` uses everything. 
`comparison` uses `analysis` and `errors`. 
`analysis`, and `user_input` uses `errors`. 
`preparation` uses `models`. 
The rest use nothing from the package, and there are no cycles. 
See [architecture.md](architecture.md).

**Can calculations be tested without files or output?** Yes. 
`analysis` and `comparison` take plain records, so tests build a few in code. 
Before, you couldn't even import the script without it reading a file and asking for input.

**Are responsibilities easier to find?** Yes. 
Each of the five (reading, preparing, calculating, presenting, coordinating) is a named module. 
Before, I had to read inside `aggregate_data` to find where typed text became a number.

**Is there less duplication?** The comparison reuses `filter_records` and `cumulative_duration`. 
The `"all countries"` string used in two places became `None`, and both modes share one year-range check. 
Some repetition remains, as `summarise_country` and the original flow in `app` both filter and then total.

**Did it add unnecessary complexity?** Some. 
It's 11 files instead of 1 and nearly 4 times the lines (much of that docstrings and the new feature), and you now follow calls across files. 
`errors.py` is three lines that exist only so the other modules can share one error type without importing each other.
I kept it to plain functions and three small dataclasses, with no frameworks and no new dependencies. 
A two or three-module split would also have worked for a program this size. 
I split by the five responsibilities because that keeps each module short and the reasons for each boundary easy to state.

## Known limitations

- An unknown country in the original mode still quietly means "all countries", as it always did. 
The comparison rejects unknown countries instead.
- A missing data file still stops the program with a normal Python error.
- EVAs with duration `0:00` (cancelled ones, for example) count as EVAs with zero hours, as before, so they pull averages down.
- Country names must match exactly (`usa` is not `USA`), as before.
- Comparing a country with itself is allowed and reports a tie.

## Decisions

- [ADR-001](adr/ADR-001-split-by-responsibility.md): split the script by
  responsibility.
- [ADR-002](adr/ADR-002-invalid-query-error.md): report bad requests with
  `InvalidQueryError`, handled in `app`.
