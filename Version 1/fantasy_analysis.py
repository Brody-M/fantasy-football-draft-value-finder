"""Phase 1: compare historical PPR points with saved draft rankings."""

import csv
import math
from pathlib import Path


def number(value):
    """Read a number from a CSV cell; keep missing or invalid values as None."""
    try:
        result = float(value)
        if math.isfinite(result):
            return result
    except (ValueError, TypeError):
        pass
    return None


def analyze(rows):
    """Group comparable players and calculate their difference in rank."""
    groups = {"QB": [], "RB": [], "WR": [], "TE": []}
    exclusions = {}

    for row in rows:
        position = row["position"]
        points = number(row["fantasy_points_ppr"])
        draft_rank = number(row["adp_consensus_rank"])
        games = number(row["games_played"])

        reason = ""
        if row["match_status"] != "matched":
            reason = "Not in both sources"
        elif position not in groups or row["adp_position"] != position:
            reason = "Different positions in the sources"
        elif points is None or draft_rank is None or draft_rank <= 0:
            reason = "Missing or invalid points / draft rank"

        if reason:
            exclusions[reason] = exclusions.get(reason, 0) + 1
            continue

        points_per_game = ""
        if games is not None and games > 0:
            points_per_game = round(points / games, 2)
        if games is None:
            games = ""

        player = {
            "player": row["player"], "position": position,
            "stats_season": "2025", "adp_season": "unverified",
            "comparison_type": "descriptive_only",
            "ppr_points": points, "games_played": games,
            "ppr_per_game": points_per_game,
            "saved_consensus_rank": draft_rank,
        }
        groups[position].append(player)

    # Rank is one plus the number of players ahead of this player.
    # Ties share a rank. Each position has its own comparison group.
    for players in groups.values():
        for player in players:
            draft_rank = 1
            points_rank = 1
            for other in players:
                if other["saved_consensus_rank"] < player["saved_consensus_rank"]:
                    draft_rank += 1
                if other["ppr_points"] > player["ppr_points"]:
                    points_rank += 1
            player["draft_rank_in_group"] = draft_rank
            player["ppr_rank_in_group"] = points_rank
            player["rank_difference"] = draft_rank - points_rank

    return groups, exclusions


def rank_difference(player):
    """Tell sorted() which value to order the players by."""
    return player["rank_difference"]


def table(title, players):
    """Make an aligned terminal table for up to three players."""
    lines = [title, f"  {'Player':<25} {'Draft':>5} {'PPR':>5} {'Gap':>5} {'Points':>7} {'Games':>5}"]
    if not players:
        lines.append("  No players to show.")
    for player in players[:3]:
        games = "--"
        if player["games_played"] != "":
            games = f"{player['games_played']:g}"
        lines.append(
            f"  {player['player']:<25} {player['draft_rank_in_group']:>5} "
            f"{player['ppr_rank_in_group']:>5} {player['rank_difference']:>+5} "
            f"{player['ppr_points']:>7.1f} {games:>5}")
    return lines


def main():
    """Load the data, analyze it, then display and save the results."""
    folder = Path(__file__).resolve().parent
    source = folder / "fantasy_football_merged.csv"
    required = ["player", "position", "match_status", "adp_position",
                "fantasy_points_ppr", "adp_consensus_rank", "games_played"]
    try:
        with source.open(encoding="utf-8-sig", newline="") as file:
            reader = csv.DictReader(file)
            for column in required:
                if column not in (reader.fieldnames or []):
                    raise ValueError("Missing column: " + column)
            rows = list(reader)
    except (OSError, ValueError) as error:
        print("Could not read the dataset:", error)
        raise SystemExit(1)

    groups, exclusions = analyze(rows)
    all_players = []
    for position in groups:
        groups[position] = sorted(groups[position], key=rank_difference, reverse=True)
        all_players.extend(groups[position])

    line = "=" * 66
    report = [line, "  FANTASY FOOTBALL | PHASE 1", line,
              "  2025 PPR production vs. saved draft order",
              "  ADP season / scoring unverified: comparisons, not predictions.", "",
              f"  Players loaded: {len(rows)}   Compared: {len(all_players)}   Skipped: {sum(exclusions.values())}",
              "  Draft and PPR are ranks within the same position group.",
              "  Gap = Draft - PPR. Positive means a better production rank."]

    for position, players in groups.items():
        report.extend(["", line, f"  {position} | {len(players)} players", line])
        positive = []
        negative = []
        for player in players:
            if player["rank_difference"] > 0:
                positive.append(player)
            elif player["rank_difference"] < 0:
                negative.append(player)
        negative = sorted(negative, key=rank_difference)
        report.extend(table("  HIGHER IN PRODUCTION (largest positive gaps)", positive))
        report.append("")
        report.extend(table("  LOWER IN PRODUCTION (largest negative gaps)", negative))

    report.extend(["", line, "  DATA NOTES", line])
    for reason, count in exclusions.items():
        report.append(f"  {count:>3} skipped: {reason}")
    report.extend(["  Missing values are not zero. Ties share ranks (1, 2, 2, 4).",
                   "  Total points reflect games played. Compare gaps within positions.",
                   "  See data_season_audit.md for the season uncertainty.", "",
                   "  Full results: player_comparison.csv",
                   "  This summary: analysis_report.txt", line])
    report_text = "\n".join(report) + "\n"

    fields = ["player", "position", "stats_season", "adp_season", "comparison_type",
              "ppr_points", "games_played", "ppr_per_game", "saved_consensus_rank",
              "draft_rank_in_group", "ppr_rank_in_group", "rank_difference"]
    with (folder / "player_comparison.csv").open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(all_players)
    (folder / "analysis_report.txt").write_text(report_text, encoding="utf-8")
    print(report_text)


if __name__ == "__main__":
    main()
