# Fantasy Football Ranking Comparison — Phase 1

## Project goal

Among players available in both sources, which players rank higher in historical PPR fantasy production than in saved draft ordering within their position?

This is the **Vibe Code** track. The supplied Phase 0 dataset is reused for Phase 1. Confirm it is available in the course's shared dataset pool, as specified in the project prompt.

## Run the program

Requires Python 3; no packages need to be installed. Open a terminal in `Version 1` and run:

```text
python fantasy_analysis.py
```

On Windows, `py fantasy_analysis.py` also works if the Python launcher is installed. The input and output paths are relative to the script, so running it from another folder also works. Each run replaces the two generated result files.

## Files

- `fantasy_analysis.py`: executable analysis, using only `csv`, `math`, `collections`, and `pathlib` from Python's standard library.
- `fantasy_football_merged.csv`: unchanged Phase 0 input.
- `dataset_description.md`: original source descriptions and preparation notes.
- `analysis_report.txt`: generated findings, group summaries, and limitations.
- `player_comparison.csv`: all eligible players and calculated rankings.
- `data_season_audit.md`: evidence for 2025 statistics and the unresolved ADP season.
- `test_fantasy_analysis.py`: checks for ties, position grouping, missing values, and exclusions. Run `python -m unittest discover -s "."` from this folder.

## How it works

1. `csv.DictReader` reads each row as a dictionary; the rows are stored in a list.
2. Keep matched players with usable PPR totals, positive saved consensus ranks, and compatible QB/RB/WR/TE positions. Missing values stay missing. Travis Hunter's CB ADP entry is excluded from a WR comparison.
3. Store eligible player dictionaries in lists grouped by position.
4. For each player, count how many eligible peers have more PPR points and how many have earlier saved draft ranks. Add one to each count to obtain the two ranks. Ties share competition ranks, such as 1, 2, 2, 4.
5. Subtract PPR rank from draft rank. For example, draft rank 20 and PPR rank 8 produce +12. This is a descriptive difference in rank, not 12 extra fantasy points.
6. Print and save results. PPR per game is supporting context; total PPR determines the production rank. Both rankings use the same player pool.

## Interpretation and limitations

The supplied notes associate the statistics with 2025, but the saved ADP snapshot's date and scoring format remain unverified. The program therefore compares two saved orderings without claiming that the ADP represented preseason expectations for those results. Total PPR reflects games played; per-game values do not establish future ability. Rank differences should be compared within positions, whose sample sizes differ. Source position/overall ranks are not used as PPR ranks.

The season audit spot-checks the statistics against the season-specific 2025 source. Each exported player row includes the statistics season, the unverified ADP season, and a descriptive-only label. Different team labels cannot establish the season of the saved numeric ADP ranks. See [the data audit](data_season_audit.md) for the evidence and the data needed for a future draft-value tool.

See `analysis_report.txt` for actual findings. The input file is preserved, including unmatched players; they are only excluded from this particular analysis.

## Phase 1 alignment

The program opens a CSV with Python, stores rows in dictionaries, groups and transforms data to answer a defined question, and presents results as terminal output plus saved files. It uses no Pandas, Polars, NumPy, or similar data-processing libraries. The parent directory contains the required plain-text version history and this `Version 1` folder contains the code, inputs, and outputs.

Assignment reference: https://docs.google.com/document/d/16RQymQe6RE-kIy2nFQPItE9qhiVA3SFtbOASzMnfw20/edit

AI assistance: OpenAI Codex generated the code and documentation from the assignment and supplied Phase 0 files. Review the code and results before submitting. This package has not been uploaded to Canvas.
