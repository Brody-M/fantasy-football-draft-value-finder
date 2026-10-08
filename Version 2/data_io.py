"""Read the player dataset and write the two result files."""

import csv
from pathlib import Path


REQUIRED_COLUMNS = {
    "player", "position", "match_status", "adp_position",
    "fantasy_points_ppr", "adp_consensus_rank", "games_played",
}

OUTPUT_COLUMNS = [
    "player", "position", "stats_season", "adp_season", "comparison_type",
    "ppr_points", "games_played", "ppr_per_game", "saved_consensus_rank",
    "draft_rank_in_group", "ppr_rank_in_group", "rank_difference",
]


def load_players(path: Path) -> list[dict[str, str]]:
    """Read CSV rows as dictionaries after checking the column names.

    Args:
        path: Location of the merged input CSV.
    Returns:
        A list of rows with column names as keys and cell text as values.
    """
    with path.open(encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        available_columns = set(reader.fieldnames or [])
        missing_columns = REQUIRED_COLUMNS - available_columns
        if missing_columns:
            raise ValueError("Missing columns: " + ", ".join(sorted(missing_columns)))
        return list(reader)


def save_players(path: Path, players: list[dict]) -> None:
    """Write every eligible player's calculated results to a CSV.

    Args:
        path: Destination CSV; each run replaces its contents.
        players: Calculated player dictionaries in display order.
    Returns:
        None.
    """
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=OUTPUT_COLUMNS)
        writer.writeheader()
        writer.writerows(players)


def save_report(path: Path, report: str) -> None:
    """Write the terminal summary to a text file.

    Args:
        path: Destination text file; each run replaces its contents.
        report: The formatted report text.
    Returns:
        None.
    """
    with path.open("w", encoding="utf-8") as file:
        file.write(report)
