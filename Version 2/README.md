# Fantasy Football - Phase 2

Phase 2 makes the working program easier to understand and change. It answers the same question as Version 1: which players rank higher in 2025 PPR production than in saved draft ordering within their position?

## Run it

From the project folder:

```text
python "Version 2/main.py"
```

Or run `python main.py` inside `Version 2`. Requires Python 3.10 or newer for the type-hint syntax; no packages are required. Each run replaces the two output files in this version. Version 1 remains the earlier snapshot.

## Four small modules

| File | Responsibility |
| --- | --- |
| `main.py` | Call the steps in order and display the finished report |
| `data_io.py` | Read the CSV and save the result files |
| `analysis.py` | Select comparable players, group them, and calculate ranks |
| `reporting.py` | Put the existing results into readable terminal tables |

Start with `main.py`: load rows, group players, add ranks, build a report, then save it. Each module owns a different job. Calculations do not print tables or open files, and reporting does not calculate player ranks.

## What changed for this phase

- **Single responsibility:** the old large functions are split into smaller functions for loading, eligibility checks, grouping, ranking, and report formatting.
- **Type hints and docstrings:** each function has input/output hints and a docstring with a summary, `Args`, and `Returns`. The `add_ranks()` docstring also explains that it updates the supplied records.
- **Repeated logic:** `gap_table()` handles selecting and displaying either positive or negative gaps instead of repeating both table-building paths in the main program.
- **Data structures:** required CSV columns use a set because they are unique and unordered. Set difference finds missing columns in one step. Player order uses lists; position groups and exclusion counts use dictionaries.
- **Comprehensions and conversions:** a dictionary comprehension creates the position lists; short list comprehensions filter positive and negative gaps. `set(reader.fieldnames or [])` converts the column list to a set, and `list(reader)` collects CSV dictionaries. `.get()` updates the reason counts.

Example to understand the set check: if the required columns are `{"player", "position"}` and the file has only `{"player"}`, their difference is `{"position"}`.

Player records contain a mix of text and numbers, so their type hint stays the simple `dict`. Raw CSV rows use the more specific `dict[str, str]`. There are no new classes or frameworks in the program.

## What the results mean

`Gap = draft rank - PPR rank`. The same eligible players are ranked within each position, and ties share ranks (1, 2, 2, 4). Missing values stay missing. The terminal shows three positive and three negative gaps per position; `player_comparison.csv` includes every eligible player.

Statistics match 2025 results. The ADP season, date, and scoring format remain unverified, so the comparison is descriptive rather than a confirmed draft recommendation. The copied [dataset description](dataset_description.md) and [season audit](data_season_audit.md) explain the existing input. No data was replaced for Phase 2.

## Remaining phases

Basic display sorting and CSV-column checks existed in Version 1 and were moved into the new modules. Phase 2 adds no new sorting method or function-precondition system. Phase 3 remains available for those improvements. Pandas and plots belong to Phase 4; the optional GUI stays on the later [timeline](../TIMELINE.md).

## Check it

```text
python -B -m unittest discover -s "Version 2"
```

Checks cover tie ranks, position groups, missing data, empty input, missing CSV columns, quoted player names, and output-file round trips. `test_phase2.py` is separate from the program and does not need to run during normal use.

Input: `fantasy_football_merged.csv`. Outputs: `analysis_report.txt` and `player_comparison.csv`. AI assistance: OpenAI Codex helped refactor and check this version. The required log is [Project Version History](../Project%20Version%20History.txt).
