# Data season audit

Checked September 17, 2026. The original input CSV has not been changed.

## What is established

The statistics match **2025 season results**, not 2026 projections. The supplied Jonathan Taylor row has 17 games, 1,585 rushing yards, 18 rushing touchdowns, and 362.3 PPR points. These values match the [2025 Pro Football Reference fantasy table](https://www.pro-football-reference.com/years/2025/fantasy.htm). This is a source spot-check supporting the earlier preparation notes, not a new verification of every row. The export itself has no season column.

## What remains uncertain

The original ADP text has no saved season, retrieval date, or scoring settings. The older filename `footballguys_2025_adp_cleaned.csv` does not establish any of those facts. The [Footballguys ADP page](https://www.footballguys.com/adp) is live; today's table cannot prove the date or settings of the saved text. Its platform columns also represent different league formats.

The merged file includes these concrete discrepancies:

| Player | Statistics team | Saved ADP team |
| --- | --- | --- |
| A.J. Brown | PHI | NE |
| Mike Evans | TAM | SF |

These labels are a reason to investigate different dates or updated metadata. They do **not** prove that the numeric draft ranks are from 2026: a source can update team labels separately from historical rankings. No season has been guessed or relabeled in the original input.

## Phase 1 decision

Compare 2025 PPR production rank with saved consensus order within the same matched QB, RB, WR, or TE group. Call the result a **descriptive rank difference**. A positive difference means a player ranks better by historical PPR production; it does not establish a preseason bargain or predict next season.

The generated player CSV carries `stats_season=2025`, `adp_season=unverified`, and `comparison_type=descriptive_only` so the qualification stays attached to exported results. ADP values are saved rank/order values, not verified average pick numbers. Scoring compatibility remains unverified.

## How to make a later draft-value analysis valid

- For a 2025 retrospective: obtain a dated **preseason 2025 PPR, one-quarterback redraft** ADP snapshot and compare it to 2025 results. Keep its URL, retrieval date, draft date range, and settings.
- For a 2026 draft tool: use verified **2026 PPR, one-quarterback redraft** ADP and label 2025 results as previous-season input. Prefer separately identified 2026 projections for a projection-based comparison; do not label 2025 totals as projected 2026 points.
- A completed 2026 season is not available as of this audit date. Do not compare partial 2026 totals to full 2025 totals as if they covered equal periods.

Before replacing the class dataset, confirm that the replacement is in the shared course pool or is permitted by the instructor. The existing Phase 0 dataset is retained for this Phase 1 package; its presence in the shared pool has not been verified here.
