"""Phase 1: compare saved draft ordering with historical PPR production."""

import csv
import math
from collections import Counter
from pathlib import Path


def number(value):
    """Convert a CSV cell to a finite number, or return None if unavailable."""
    if value is None or not value.strip():
        return None
    try:
        result = float(value)
        return result if math.isfinite(result) else None
    except ValueError:
        return None


def analyze(rows):
    """Return position groups with comparable ranks, plus exclusion counts."""
    groups = {position: [] for position in ("QB", "RB", "WR", "TE")}
    exclusions = Counter()
    for row in rows:
        position = row["position"]
        if row["match_status"] != "matched":
            exclusions["Not present in both sources"] += 1
            continue
        if position not in groups or row["adp_position"] != position:
            exclusions["Incompatible position"] += 1
            continue
        points = number(row["fantasy_points_ppr"])
        draft_rank = number(row["adp_consensus_rank"])
        games = number(row["games_played"])
        if points is None or draft_rank is None or draft_rank <= 0:
            exclusions["Missing or invalid points/draft rank"] += 1
            continue
        groups[position].append({
            "player": row["player"], "position": position,
            "stats_season": "2025", "adp_season": "unverified",
            "comparison_type": "descriptive_only",
            "ppr_points": points, "saved_consensus_rank": draft_rank,
            "games_played": games if games is not None else "",
            "ppr_per_game": round(points / games, 2) if games and games > 0 else "",
        })

    for players in groups.values():
        for player in players:
            # Competition ranks: ties share a rank, e.g. 1, 2, 2, 4.
            player["draft_rank_in_group"] = 1 + sum(
                other["saved_consensus_rank"] < player["saved_consensus_rank"]
                for other in players
            )
            player["ppr_rank_in_group"] = 1 + sum(
                other["ppr_points"] > player["ppr_points"] for other in players
            )
            player["rank_difference"] = (
                player["draft_rank_in_group"] - player["ppr_rank_in_group"]
            )
    return groups, exclusions


def main():
    """Read the saved CSV and write a report and player comparison beside it."""
    folder = Path(__file__).resolve().parent
    source = folder / "fantasy_football_merged.csv"
    required = {"player", "position", "match_status", "adp_position",
                "fantasy_points_ppr", "adp_consensus_rank", "games_played"}
    try:
        with source.open(encoding="utf-8-sig", newline="") as file:
            reader = csv.DictReader(file)
            missing = required - set(reader.fieldnames or [])
            if missing:
                raise ValueError("Missing columns: " + ", ".join(sorted(missing)))
            rows = list(reader)
        groups, exclusions = analyze(rows)
    except (OSError, ValueError) as error:
        raise SystemExit(f"Could not analyze dataset: {error}") from error

    fields = ["player", "position", "stats_season", "adp_season", "comparison_type",
              "ppr_points", "games_played", "ppr_per_game",
              "saved_consensus_rank", "draft_rank_in_group", "ppr_rank_in_group",
              "rank_difference"]
    output = folder / "player_comparison.csv"
    with output.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        for players in groups.values():
            writer.writerows(sorted(players, key=lambda p: (-p["rank_difference"], p["player"])))

    lines = ["FANTASY FOOTBALL: PPR PRODUCTION AND SAVED DRAFT ORDERING",
             "", "Question: Which players rank higher in PPR production than in",
             "saved draft ordering within the same eligible position group?", "",
             f"Input: {source.name}", f"Total dataset rows: {len(rows)}",
             f"Source coverage: {dict(Counter(row['match_status'] for row in rows))}",
             f"Included: {sum(len(players) for players in groups.values())}",
             f"Excluded: {sum(exclusions.values())}"]
    lines.extend(f"  {reason}: {count}" for reason, count in exclusions.items())
    lines += ["", "METHOD",
              "Use matched QB/RB/WR/TE players with compatible ADP positions and",
              "available PPR points and positive consensus draft ranks. Recompute",
              "both rankings within the identical eligible position group.",
              "Rank difference = draft rank in group minus PPR rank in group.",
              "Positive means a better PPR rank; negative means a worse PPR rank.",
              "Ties use competition ranks (1, 2, 2, 4). PPR/game is context only.",
              "", "LIMITATIONS",
              "Statistics match 2025 season data. The saved ADP season, snapshot",
              "date and scoring format are unverified. Team labels differ across",
              "sources; do not infer the ranking season from team labels alone.",
              "See data_season_audit.md for evidence. These differences are",
              "descriptive, not confirmed preseason value or future predictions.",
              "Total points reflect availability as well as production. Missing",
              "values are not zero. Excluded players are not automatically sleepers.",
              "Position groups have different sizes; compare gaps within positions."]
    for position, players in groups.items():
        lines += ["", f"{position} ({len(players)} eligible players)"]
        if not players:
            lines.append("No eligible players.")
            continue
        lines.append(f"Mean PPR total: {sum(p['ppr_points'] for p in players)/len(players):.1f}")
        for label, selection in (
            ("Largest positive differences", sorted(
                (p for p in players if p["rank_difference"] > 0),
                key=lambda p: (-p["rank_difference"], p["player"]))[:5]),
            ("Largest negative differences", sorted(
                (p for p in players if p["rank_difference"] < 0),
                key=lambda p: (p["rank_difference"], p["player"]))[:5]),
        ):
            lines.append(label + ":")
            for player in selection:
                lines.append(
                    f"  {player['player']}: draft {player['draft_rank_in_group']}, "
                    f"PPR {player['ppr_rank_in_group']}, gap {player['rank_difference']:+d}; "
                    f"{player['ppr_points']:.1f} points, {player['games_played']} games")
            if not selection:
                lines.append("  None")
    report = "\n".join(lines) + "\n"
    (folder / "analysis_report.txt").write_text(report, encoding="utf-8")
    print(report)
    print("Saved analysis_report.txt and player_comparison.csv beside this script.")


if __name__ == "__main__":
    main()
