# ADR-002: Report bad requests with one exception, handled in `app`

## Context

The country comparison has to cope with reversed years, non-numeric years and unknown countries without crashing. 
Two places can spot a bad request: `user_input.py` sees the typed text, and `comparison.py` knows the rules (start year not after end year, both countries exist). 
The inherited code just crashed with a raw ValueError or ZeroDivisionError.

Either layer needs a way to say "this request is invalid" without printing, exiting, or depending on the other.

## Alternatives

1. **Re-prompt inside `user_input.py` until the answer is valid.** 
User-friendly, but `user_input.py` would need the data and the domain rules, and none of it could be tested without faking a console.
2. **Return `None` or an error value from `compare_countries`.** 
Every caller has to remember to check, and there's nowhere to put a message.
3. **Let `ValueError` bubble up and catch it in `app.py`.**
Simple, but catching `ValueError` that broadly would also hide real bugs.
4. **A dedicated `InvalidQueryError` in its own small module.** 
This was the chosen method.

## Decision

Add `eva/errors.py` with `InvalidQueryError(ValueError)`. 
`analysis`, `comparison` and `user_input` raise it. 
Only `app` catches it (in `run_country_comparison` and `run_cumulative_analysis`), prints `Cannot compare: <reason>` or `Cannot analyse: <reason>`, and returns normally.

## Rationale

- `comparison` stays a pure function. Invalid input is tested with `assertRaises`, no console needed.
- The lower layers describe the problem and `app` decides how to tell the user.
- A narrow exception type doesn't swallow unrelated bugs.
- A separate module means `user_input` and `comparison` don't import each other.

## Consequences

Good:

- Every invalid-input path, in both modes, has a test and ends in a readable message instead of a traceback.
- Both modes share the same year-range check.

Costs:

- One more tiny module and one more exception to know about.
- Handling the original mode this way changed its behaviour for inputs that used to crash. 
That was a separate commit from the refactor and the feature, so those two stayed behaviour-preserving.
- The program exits with status 0 after printing the error. 
A later change could return a non-zero code.
