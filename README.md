# Fantasy Football Draft Value Finder

A beginner Python semester project comparing 2025 PPR production with saved draft rankings. Phase 2 refactors the working analysis into small modules with type hints and docstrings. The ADP season and scoring settings remain unverified, so the output is a descriptive comparison rather than a prediction.

```text
python "Version 2/main.py"
```

Python 3.10 or newer is required; no packages are needed. The terminal displays aligned position tables. All results are saved in Version 2 beside the program.

- [Phase 2 code and instructions](Version%202/README.md)
- [Latest report](Version%202/analysis_report.txt)
- [Earlier Phase 1 snapshot](Version%201/README.md)
- [Semester timeline and later GUI idea](TIMELINE.md)
- [Version history](Project%20Version%20History.txt)
- [Data season audit](Version%201/data_season_audit.md)

## Project layout

```text
Version 1/                   Earlier Phase 1 snapshot
Version 2/                   Phase 2 modules, input CSV, outputs, notes, tests
data/raw/                    Original source exports for reference
Project Version History.txt  Course version log
TIMELINE.md                  Required phases and optional GUI plan
README.md                    Start here
```

Old cleaning experiments and empty phase guides were removed from the active GitHub tree. Earlier preparation files remain available in Git history. Original source exports are retained for checking provenance. Each course version keeps its own input and output files so the earlier snapshot remains runnable.

Run current checks with `python -B -m unittest discover -s "Version 2"`. Confirm the input dataset is in the shared course pool before submitting. AI assistance: OpenAI Codex helped prepare, implement, simplify, and refactor the project.
