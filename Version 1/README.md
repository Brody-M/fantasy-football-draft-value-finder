# Fantasy Football - Phase 1

Which players rank higher in 2025 PPR production than in the saved draft ordering within their position?

## Run it

Open a terminal in this folder and run:

```text
python fantasy_analysis.py
```

Python 3 is all you need. No extra packages. You can also run `python "Version 1/fantasy_analysis.py"` from the parent folder. File paths follow the script, so it works from other folders too.

The terminal shows the top three positive and negative rank differences for each position. `Draft` and `PPR` are ranks in the same eligible position group; `Points` is total PPR production. Each run replaces `analysis_report.txt` with the same summary and `player_comparison.csv` with all eligible players.

## Read the code in this order

1. `number()` converts CSV text into numbers. Missing values stay missing.
2. `analyze()` puts players in QB, RB, WR, and TE lists. Simple loops count how many players rank ahead of each player.
3. `rank_difference()` tells `sorted()` which value to use.
4. `table()` lines up the terminal columns. The formatting numbers control column width.
5. `main()` reads the CSV, calls the analysis, and saves and prints results.

The code uses ordinary loops, lists, and dictionaries in one file. No classes, pandas, terminal packages, or GUI are needed to run it. The separate test file uses Python's built-in test library and is only for checking the calculations.

## What the numbers mean

`Gap = draft rank - PPR rank`. Draft rank 20 and PPR rank 8 give a gap of +12. That means 12 places higher in production, not 12 extra points. Ties share ranks, such as 1, 2, 2, 4. Both ranks use the same eligible player pool within a position. Total points determine rank; points per game remain in the full CSV for context.

The statistics match 2025 results, but the ADP season and scoring format remain unverified. These results are descriptive comparisons, not confirmed sleepers or busts. Total points also reflect games played. Missing data is not zero, and unmatched players are not automatically sleepers. Read [the season audit](data_season_audit.md) for evidence.

## Files

| File | Purpose |
| --- | --- |
| `fantasy_analysis.py` | The program |
| `fantasy_football_merged.csv` | The one input dataset |
| `analysis_report.txt` | Saved terminal summary |
| `player_comparison.csv` | All results, including season labels |
| `dataset_description.md` | Column guide and preparation notes |
| `data_season_audit.md` | Date/scoring uncertainty and next data steps |
| `test_fantasy_analysis.py` | Calculation checks |

Run the checks with `python -m unittest discover -s "."` from this folder.

This is the Vibe Code track: read a CSV, store dictionaries, organize and calculate results, then present them using standard Python. Confirm the dataset is in the class's shared pool before submitting. The parent folder has the required version history and a [timeline](../TIMELINE.md), including a later GUI idea.

AI assistance: OpenAI Codex helped write and simplify this project. It has not been submitted to Canvas.
