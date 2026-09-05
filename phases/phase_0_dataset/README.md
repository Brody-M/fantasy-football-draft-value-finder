# Phase 0: Dataset

Status: Prepared for submission.

Submit the [CSV](../../data/processed/fantasy_football_merged.csv) and the submission paragraph in the [dataset description](../../docs/dataset_description.md).

The file contains 651 players and 33 columns, exceeding the suggested 20 rows and five columns.

Preparation repaired 55 shifted ADP rows, removed one duplicate statistics entry, and preserved unmatched players with a status label.

To rebuild, run `python phases/phase_0_dataset/prepare_dataset.py` from the repository folder. Inputs are the original ADP text and existing cleaned statistics. The original statistics export is retained for reference.
