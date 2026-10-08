"""Run the Phase 2 fantasy football comparison."""

from pathlib import Path

from analysis import add_ranks, group_players
from data_io import load_players, save_players, save_report
from reporting import build_report, display_groups


def main() -> None:
    """Coordinate loading, analysis, reporting, and saving.

    Args:
        None. Input and output paths are relative to this script.
    Returns:
        None. Results are printed and saved beside the script.
    """
    folder = Path(__file__).resolve().parent
    try:
        rows = load_players(folder / "fantasy_football_merged.csv")
        groups, exclusions = group_players(rows)
        add_ranks(groups)
        groups = display_groups(groups)

        # Convert the dictionary's position lists into one list for the CSV.
        all_players = []
        for players in groups.values():
            all_players.extend(players)

        report = build_report(groups, exclusions, len(rows))
        save_players(folder / "player_comparison.csv", all_players)
        save_report(folder / "analysis_report.txt", report)
    except (OSError, ValueError) as error:
        print("Could not complete the comparison:", error)
        raise SystemExit(1)
    print(report)


if __name__ == "__main__":
    main()
