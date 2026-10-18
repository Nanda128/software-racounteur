# ADR-001: Split the single script into modules by responsibility

## Context

The EVA app was one script where reading, cleaning, analysis, output and control flow were tangled together. 
Importing it ran the whole program. 
The main functions read global variables, so they couldn't be run on test data, and one function took raw typed text and did the filtering, totalling and counting. 
A single file isn't allowed, and the new country-comparison feature needed to reuse the existing calculations.

## Alternatives

1. **Keep one file and tidy it** (add `main()`, remove globals). 
Cheap, but everything is still in one place.
2. **Split by the existing function list** (`functions.py`, `helpers.py`).
That gives several files but arbitrary boundaries, with unrelated functions sharing a module.
3. **Split by responsibility into one flat package.** 
Chosen.
4. **Classes, interfaces and dependency injection** (repositories, services).
Decouples well, but adds machinery a program this size doesn't need.

## Decision

Create the `eva/` package with `data_source`, `preparation`, `models`, `analysis`, `presentation`, `user_input` and `app`. 
Keep `evacodev2.py` as a thin entry point. 
Modules talk through plain functions and one small dataclass, `EvaRecord`. 
There is no module-level state. 
Only `app` depends on everything else.

## Rationale

- Each module changes for one reason, so a new file format or a new output only touches one place.
- Passing data as arguments removes the global-state coupling.
- Pure functions in `analysis` can be tested with a few handwritten records.
- Functions and one dataclass are the smallest thing that works. Alternative 4 was more than the job needed.
- The comparison feature can be a new module on top of `analysis` without touching loading or preparation.

## Consequences

Good:

- Changes to the file format, cleaning rules, statistics, output or prompts each stay in one module.
- Calculations can be unit tested and reused.

Costs:

- More files and imports to follow in a small program.
- `preparation` and `analysis` both depend on the shape of `EvaRecord`, so changing a field touches both.
- `app.py` knows every module. It has to stay free of logic, or it becomes the new monolith.
- There were no tests at the start, so "behaviour unchanged" had to be shown by comparing outputs before and after.
