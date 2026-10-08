"""Select comparable players and calculate ranks within each position."""

import math


POSITIONS = ["QB", "RB", "WR", "TE"]


def number(value: str | None) -> float | None:
    """Convert cell text to a finite number while keeping missing data missing.

    Args:
        value: Text from a CSV cell, or None.
    Returns:
        A number, or None for blank, invalid, or non-finite values.
    """
    try:
        result = float(value)
        if math.isfinite(result):
            return result
    except (ValueError, TypeError):
        pass
    return None


def exclusion_reason(row: dict[str, str], points: float | None,
                     draft_rank: float | None) -> str:
    """Explain why a row cannot be used in this comparison.

    Args:
        row: One input player row.
        points: Converted PPR total, or None.
        draft_rank: Converted saved draft rank, or None.
    Returns:
        An exclusion reason, or an empty string when the row is eligible.
    """
    if row["match_status"] != "matched":
        return "Not in both sources"
    if row["position"] not in POSITIONS or row["adp_position"] != row["position"]:
        return "Different positions in the sources"
    if points is None or draft_rank is None or draft_rank <= 0:
        return "Missing or invalid points / draft rank"
    return ""


def group_players(rows: list[dict[str, str]]) -> tuple[dict[str, list[dict]], dict[str, int]]:
    """Convert eligible rows into player records grouped by position.

    Args:
        rows: Raw CSV dictionaries returned by load_players().
    Returns:
        Position lists of numeric player records, and counts by exclusion reason.
    """
    groups = {position: [] for position in POSITIONS}
    exclusions = {}
    for row in rows:
        points = number(row["fantasy_points_ppr"])
        draft_rank = number(row["adp_consensus_rank"])
        reason = exclusion_reason(row, points, draft_rank)
        if reason:
            exclusions[reason] = exclusions.get(reason, 0) + 1
            continue

        games = number(row["games_played"])
        points_per_game = ""
        if games is not None and games > 0:
            points_per_game = round(points / games, 2)
        if games is None:
            games = ""

        player = {
            "player": row["player"], "position": row["position"],
            "stats_season": "2025", "adp_season": "unverified",
            "comparison_type": "descriptive_only",
            "ppr_points": points, "games_played": games,
            "ppr_per_game": points_per_game,
            "saved_consensus_rank": draft_rank,
        }
        groups[row["position"]].append(player)
    return groups, exclusions


def add_ranks(groups: dict[str, list[dict]]) -> None:
    """Add draft rank, PPR rank, and their difference to each player record.

    Args:
        groups: Eligible player records grouped by position; updated in place.
    Returns:
        None. The records in groups gain three calculated fields.
    """
    # Same counting method as Version 1: ties share ranks (1, 2, 2, 4).
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
