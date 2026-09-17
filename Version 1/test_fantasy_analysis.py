"""Small standard-library checks for ranking and missing-data behavior."""

import unittest

from fantasy_analysis import analyze, number


def row(name, points, draft, position="WR", **changes):
    """Build an example input row with the fields used by the analysis."""
    result = dict(player=name, fantasy_points_ppr=str(points),
                  adp_consensus_rank=str(draft), games_played="10",
                  position=position, adp_position=position, match_status="matched")
    result.update(changes)
    return result


class AnalysisTests(unittest.TestCase):
    def test_missing_values_are_not_zero(self):
        for value in (None, "", "-", "NaN", "inf"):
            self.assertIsNone(number(value))
        self.assertEqual(number("0"), 0)

    def test_ties_and_position_groups(self):
        groups, excluded = analyze([
            row("A", 100, 30), row("B", 100, 10), row("C", 50, 20),
            row("D", 500, 1, position="QB")])
        players = {p["player"]: p for group in groups.values() for p in group}
        self.assertEqual(players["A"]["rank_difference"], 2)
        self.assertEqual(players["B"]["ppr_rank_in_group"], 1)
        self.assertEqual(players["C"]["ppr_rank_in_group"], 3)
        self.assertEqual(players["D"]["rank_difference"], 0)
        self.assertEqual(players["A"]["adp_season"], "unverified")
        self.assertFalse(excluded)

    def test_exclusions_and_zero_games(self):
        groups, excluded = analyze([
            row("Unmatched", 20, 1, match_status="stats_only"),
            row("Position mismatch", 20, 2, adp_position="CB"),
            row("Missing", "", 3), row("Invalid rank", 10, 0),
            row("Zero", 0, 5, games_played="0")])
        self.assertEqual(sum(excluded.values()), 4)
        self.assertEqual(len(groups["WR"]), 1)
        self.assertEqual(groups["WR"][0]["ppr_per_game"], "")

    def test_empty_input(self):
        groups, excluded = analyze([])
        self.assertTrue(all(not players for players in groups.values()))
        self.assertFalse(excluded)


if __name__ == "__main__":
    unittest.main()
