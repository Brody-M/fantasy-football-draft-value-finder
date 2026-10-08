"""Format the existing position tables and summary for the terminal."""


def rank_difference(player: dict) -> int:
    """Return the display sort value already used in Version 1.

    Args:
        player: A player record with a calculated rank difference.
    Returns:
        The player's rank difference.
    """
    return player["rank_difference"]


def display_groups(groups: dict[str, list[dict]]) -> dict[str, list[dict]]:
    """Put each position's results in the existing terminal display order.

    Args:
        groups: Player records with calculated ranks, grouped by position.
    Returns:
        New position lists ordered from largest to smallest rank difference.
    """
    ordered = {}
    for position, players in groups.items():
        ordered[position] = sorted(players, key=rank_difference, reverse=True)
    return ordered


def table(title: str, players: list[dict]) -> list[str]:
    """Format an aligned table containing up to three players.

    Args:
        title: Heading shown above the table.
        players: Player records in the order to display.
    Returns:
        A list of text lines for the heading, column names, and player rows.
    """
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


def gap_table(players: list[dict], positive: bool) -> list[str]:
    """Select one direction of rank differences and format its table.

    Args:
        players: Calculated players ordered by descending rank difference.
        positive: True for positive gaps; False for negative gaps.
    Returns:
        Lines for the selected table, with the largest gaps first.
    """
    if positive:
        selected = [player for player in players if player["rank_difference"] > 0]
        title = "  HIGHER IN PRODUCTION (largest positive gaps)"
    else:
        selected = [player for player in players if player["rank_difference"] < 0]
        selected = sorted(selected, key=rank_difference)
        title = "  LOWER IN PRODUCTION (largest negative gaps)"
    return table(title, selected)


def build_report(groups: dict[str, list[dict]], exclusions: dict[str, int],
                 total_rows: int) -> str:
    """Build the terminal report without printing or writing files.

    Args:
        groups: Position lists in display order, containing calculated ranks.
        exclusions: Number of skipped rows for each reason.
        total_rows: Number of rows loaded from the input CSV.
    Returns:
        The complete report as a single string ending with a newline.
    """
    included = 0
    for players in groups.values():
        included += len(players)

    line = "=" * 66
    report = [line, "  FANTASY FOOTBALL | PHASE 2", line,
              "  2025 PPR production vs. saved draft order",
              "  ADP season / scoring unverified: comparisons, not predictions.", "",
              f"  Players loaded: {total_rows}   Compared: {included}   Skipped: {sum(exclusions.values())}",
              "  Draft and PPR are ranks within the same position group.",
              "  Gap = Draft - PPR. Positive means a better production rank."]

    for position, players in groups.items():
        report.extend(["", line, f"  {position} | {len(players)} players", line])
        report.extend(gap_table(players, True))
        report.append("")
        report.extend(gap_table(players, False))

    report.extend(["", line, "  DATA NOTES", line])
    for reason, count in exclusions.items():
        report.append(f"  {count:>3} skipped: {reason}")
    report.extend(["  Missing values are not zero. Ties share ranks (1, 2, 2, 4).",
                   "  Total points reflect games played. Compare gaps within positions.",
                   "  See data_season_audit.md for the season uncertainty.", "",
                   "  Full results: player_comparison.csv",
                   "  This summary: analysis_report.txt", line])
    return "\n".join(report) + "\n"
