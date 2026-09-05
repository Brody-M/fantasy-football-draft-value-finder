# Fantasy Football Player Statistics and Draft Rankings

## Submission description

Category: Sports / NFL / Fantasy Football

This dataset combines historical NFL player statistics with saved Footballguys Average Draft Position (ADP) rankings. It contains 651 players and 33 columns, including player names, positions, teams, ages, games played, fantasy points under several scoring systems, and consensus and platform-specific draft ranks. There are 278 players present in both sources, 364 with statistics only, and nine with ADP data only. A `match_status` column identifies these groups, and blank cells mean unavailable data rather than zero. The dataset can support questions about how player performance relates to draft rankings within each position. The statistics align with the 2025 season, but the ADP snapshot's date and scoring format are unverified, so it should not yet be treated as a confirmed comparison of 2025 preseason expectations with 2025 results.

## Sources and period

- Statistics: the supplied `NFLData.csv`, a Sports Reference export, and its reduced version, `NFLData_cleaned.csv`. All numeric values in the cleaned file were checked against the raw export. The figures align with the 2025 summary on [Pro Football Reference's Fantasy Tools page](https://www.pro-football-reference.com/fantasy/index.htm). The local export does not include a season field.
- Draft rankings: the supplied `adp.txt`, corresponding to the [Footballguys ADP table](https://www.footballguys.com/adp). The existing cleaned file is named `footballguys_2025_adp_cleaned.csv`, but a filename alone does not establish the snapshot date. The saved ranks were preserved; live website values were not substituted. Team labels differ between the two supplied sources and are retained separately.

## Preparation and matching

- Reparsed the original ADP text and repaired 55 rows where a line break between player name and position had shifted columns in the existing cleaned CSV. All 350 repaired ADP records have the expected 24 source fields.
- Excluded 32 team-defense entries and 31 kickers because the supplied statistics cover offensive players. Retained 287 ADP player entries.
- Removed one duplicate Elijah Moore row for Denver with zero games. Retained his Buffalo row with nine games. This leaves 642 statistics records.
- Matched players using names and compatible positions. Ignored punctuation, capitalization, spaces, and trailing suffixes for matching while retaining the original source names. Used explicit aliases for Ken/Kenneth Walker, Hollywood/Marquise Brown, and Joshua/Josh Palmer. No approximate-name matching was used.
- Grouped fullbacks with running backs in `position`, preserving the original `FB` in `stats_position`. Matched Travis Hunter's ADP cornerback entry to his statistics wide-receiver entry by explicit exception; both original positions remain visible. His `CB1` ADP position rank must not be compared with wide-receiver ranks.
- Preserved players found in either source. Converted missing markers to blank cells without inventing scores. Removed nine ADP platform columns that contain no values for the retained players, plus the statistics table's original row number.
- Preserved original draft ranks, including the source's missing consensus rank 271. Do not assume ranks are consecutive after filtering players.

## Column guide

| Columns | Meaning |
| --- | --- |
| `player`, `position` | Combined player name and position group; stats name preferred when available. |
| `stats_player_name`, `adp_player_name` | Original names from each source. |
| `stats_position`, `adp_position` | Original position labels before matching adjustments. |
| `stats_team`, `adp_team` | Team abbreviations exactly as supplied; they may use different conventions or refer to different dates. `2TM`/`3TM` indicate multiple teams; `FA` is the ADP source's free-agent label. |
| `adp_bye_week` | Bye week supplied by the ADP source; its season is unverified. |
| `match_status` | `matched`, `stats_only`, or `adp_only`. |
| `age`, `games_played`, `games_started` | Values from the statistics source. |
| `fantasy_points_standard`, `fantasy_points_ppr` | Source `FantPt` and `PPR` totals; PPR includes points per reception. |
| `fantasy_points_draftkings`, `fantasy_points_fanduel` | Source `DKPt` and `FDPt` fantasy-point totals. |
| `stats_value_based_drafting` | Source `VBD` value, retained as supplied; this is not a newly calculated draft-value score. |
| `stats_position_rank`, `stats_overall_rank` | Source `PosRank` and `OvRank`; do not assume these rank PPR points. |
| `adp_consensus_rank`, `adp_position_rank` | Consensus order and the numeric part of the source position rank. Lower numbers indicate earlier ordering. |
| Remaining `adp_*_rank` columns | Source ranking values for BestBall10s, CBS, DraftKings, Drafters, ESPN, MFL, NFFC, RT Sports, Sleeper Redraft, Underdog, and Yahoo. These are saved rank values, not verified decimal average pick numbers. |

## Possible analysis and limitations

A useful question is: Among players with both sources available, which players rank higher in historical PPR production than in the saved draft ordering within their position?

For that analysis, select one scoring format, require both relevant numeric fields, and recompute both ranks within the same matched position group. Source rank columns use broader player pools and potentially different scoring rules. Exclude incompatible position entries such as Hunter's cornerback ADP rank from a wide-receiver rank comparison. Check the ADP date and league settings before interpreting differences as historical draft value or future recommendations. Missing statistics are not evidence that a player scored zero, and unmatched players are not automatically sleepers.
