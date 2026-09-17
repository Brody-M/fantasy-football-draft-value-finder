# Fantasy Football Draft Value Finder

ITSC semester project comparing NFL fantasy statistics with saved draft rankings.

**Current status:** Phase 1 implemented and checked. Phases 2 through 4 remain planned.

Run `python "Version 1/fantasy_analysis.py"` from the repository folder. No packages are required. See [Version 1](Version%201/README.md), [results](Version%201/analysis_report.txt), and the [season audit](Version%201/data_season_audit.md). The shared-pool eligibility of the supplied dataset still needs confirmation before submission.

## Dataset

- [Merged CSV](data/processed/fantasy_football_merged.csv)
- [Description, columns, and cleaning notes](docs/dataset_description.md)
- 651 players, 33 columns, and 278 players matched across both sources.
- Unmatched players are retained. Blank values mean missing data, not zero.

The statistics align with 2025 results. The ADP snapshot date and scoring format still need verification. Use this data for exploration before drawing draft-value conclusions.

## Project phases

| Phase | Work | Status |
| --- | --- | --- |
| [0: Dataset](phases/phase_0_dataset/) | Combine data and describe it | Prepared |
| [1: Initial program](phases/phase_1_initial_program/) | Read CSV data and answer a question using standard Python | Implemented |
| [2: Refactoring](phases/phase_2_refactoring/) | Functions, docstrings, modules, and better data structures | Planned |
| [3: Sorting and validation](phases/phase_3_sorting_validation/) | Custom sorting keys and function preconditions | Planned |
| [4: Pandas](phases/phase_4_pandas/) | DataFrames and plots | Planned |

**Course rule:** Do not use pandas, Polars, or similar libraries in Phase 1. Pandas is introduced in Phase 4.

## Folder layout

```text
data/
  raw/            Original statistics and ADP text
  intermediate/   Existing cleaned statistics used by the merge
  processed/      Submission CSV
docs/             Dataset description
phases/           One guide for each project phase
Version 1/        Self-contained Phase 1 code, input, outputs, and checks
Project Version History.txt  Required course version log
archive/          Earlier scripts and the superseded ADP CSV
```

## Rebuild the dataset

With Python 3 installed, run this from the repository folder:

```bash
python phases/phase_0_dataset/prepare_dataset.py
```

The script uses Python's standard library. No packages are required. It replaces the processed CSV and prints the merge counts.

## Phase 1 question

Which players rank better in historical fantasy production than in the saved draft ordering within their position?

The implemented difference is `draft_rank_in_group - ppr_rank_in_group`, calculated within identical eligible position groups. Positive means a better historical PPR rank than saved draft rank. Because ADP season and scoring settings are unverified, this is a descriptive comparison, not confirmed draft value. The run includes 273 players from 651 input rows.

Run the checks with `python -m unittest discover -s "Version 1"`. Four checks cover ties, position groups, missing data, exclusions, and empty input.

## Sources

- [Sports Reference / Pro Football Reference](https://www.pro-football-reference.com/fantasy/index.htm)
- [Footballguys ADP](https://www.footballguys.com/adp)

The dataset comes from supplied exports. AI assisted with preparation and repository setup. Source data retains its original ownership.
