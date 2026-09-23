# Fantasy Football Draft Value Finder

A beginner Python semester project comparing 2025 PPR production with saved draft rankings. Phase 1 is complete; the ADP season and scoring settings remain unverified, so the output is a descriptive comparison rather than a prediction.

```text
python "Version 1/fantasy_analysis.py"
```

No packages are required. The terminal displays aligned position tables. All results are saved beside the program.

- [Phase 1 code and instructions](Version%201/README.md)
- [Latest report](Version%201/analysis_report.txt)
- [Semester timeline and later GUI idea](TIMELINE.md)
- [Version history](Project%20Version%20History.txt)
- [Data season audit](Version%201/data_season_audit.md)

## Project layout

```text
Version 1/                   Working program, one input CSV, outputs, notes, tests
data/raw/                    Original source exports for reference
Project Version History.txt  Course version log
TIMELINE.md                  Required phases and optional GUI plan
README.md                    Start here
```

Old cleaning experiments, duplicate datasets and descriptions, and empty phase guides have been removed from the active GitHub tree. Earlier files and the Phase 0 rebuilding script remain available in Git history. Original source exports are retained for checking provenance; Phase 1 reads only `Version 1/fantasy_football_merged.csv`.

Run checks with `python -m unittest discover -s "Version 1"`. Confirm the input dataset is in the shared course pool before submitting. AI assistance: OpenAI Codex helped prepare, implement, and simplify the project.
