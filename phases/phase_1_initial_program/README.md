# Phase 1: Initial Program

Status: Implemented and checked (September 17, 2026).

The self-contained submission is in [Version 1](../../Version%201/README.md). It uses Python's standard library to read the CSV into dictionaries, group comparable players by position, compute rank differences, and save a report and detailed CSV.

From the repository root:

```text
python "Version 1/fantasy_analysis.py"
python -m unittest discover -s "Version 1"
```

See the [season audit](../../Version%201/data_season_audit.md): statistics match 2025 results, but the ADP season/date/settings remain unverified. Results are descriptive, not predictions. Confirm the supplied dataset is in the course's shared pool before submitting.

The required version name and number are in [Project Version History](../../Project%20Version%20History.txt). Phases 2-4 have not been implemented.
