"""Check the refactored calculations and CSV boundaries with small examples."""

import csv
import tempfile
import unittest
from pathlib import Path

from analysis import add_ranks, group_players, number
from data_io import load_players, save_players, save_report
from reporting import build_report, display_groups


def row(name, points, draft, position="WR", **changes):
    """Make a small raw CSV-style record for the checks."""
    result = dict(player=name, fantasy_points_ppr=str(points),
                  adp_consensus_rank=str(draft), games_played="10",
                  position=position, adp_position=position, match_status="matched")
    result.update(changes)
    return result


class Phase2Tests(unittest.TestCase):
    def test_missing_values_are_not_zero(self):
        for value in (None, "", "-", "NaN", "inf"):
            self.assertIsNone(number(value))
        self.assertEqual(number("0"), 0)

    def test_ties_and_position_groups(self):
        groups, excluded = group_players([
            row("A", 100, 30), row("B", 100, 10), row("C", 50, 20),
            row("D", 500, 1, position="QB")])
        add_ranks(groups)
        players = {p["player"]: p for group in groups.values() for p in group}
        self.assertEqual(players["A"]["rank_difference"], 2)
        self.assertEqual(players["B"]["ppr_rank_in_group"], 1)
        self.assertEqual(players["C"]["ppr_rank_in_group"], 3)
        self.assertEqual(players["D"]["rank_difference"], 0)
        self.assertEqual(players["A"]["adp_season"], "unverified")
        self.assertFalse(excluded)

    def test_exclusions_and_zero_games(self):
        groups, excluded = group_players([
            row("Unmatched", 20, 1, match_status="stats_only"),
            row("Position mismatch", 20, 2, adp_position="CB"),
            row("Missing", "", 3), row("Invalid rank", 10, 0),
            row("Zero", 0, 5, games_played="0")])
        add_ranks(groups)
        self.assertEqual(sum(excluded.values()), 4)
        self.assertEqual(len(groups["WR"]), 1)
        self.assertEqual(groups["WR"][0]["ppr_per_game"], "")

    def test_empty_input(self):
        groups, excluded = group_players([])
        add_ranks(groups)
        report = build_report(display_groups(groups), excluded, 0)
        self.assertIn("Compared: 0", report)
        self.assertIn("No players to show.", report)

    def test_missing_columns(self):
        with tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parent) as temporary:
            path = Path(temporary) / "input.csv"
            path.write_text("player,position\nA,WR\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "Missing columns:"):
                load_players(path)

    def test_csv_and_report_round_trip(self):
        with tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parent) as temporary:
            folder = Path(temporary)
            source = folder / "input.csv"
            example = row("Example, Jr.", 100, 10)
            with source.open("w", encoding="utf-8", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=list(example))
                writer.writeheader()
                writer.writerow(example)
            rows = load_players(source)
            self.assertEqual(rows[0]["player"], "Example, Jr.")
            groups, excluded = group_players(rows)
            add_ranks(groups)
            report = build_report(display_groups(groups), excluded, len(rows))
            save_players(folder / "results.csv", groups["WR"])
            save_report(folder / "report.txt", report)
            with (folder / "results.csv").open(encoding="utf-8", newline="") as file:
                saved = list(csv.DictReader(file))
            self.assertEqual(saved[0]["rank_difference"], "0")
            self.assertEqual(saved[0]["adp_season"], "unverified")
            self.assertEqual((folder / "report.txt").read_text(encoding="utf-8"), report)


if __name__ == "__main__":
    unittest.main()
