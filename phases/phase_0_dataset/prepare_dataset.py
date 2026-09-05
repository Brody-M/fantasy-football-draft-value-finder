"""Repair the supplied ADP text and prepare a checked player-level merge."""
import csv
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "data/raw"
OUTPUT = ROOT / "data/processed/fantasy_football_merged.csv"

def normalize_name(name):
    """Create a matching key while retaining original names in the output."""
    name = re.sub(r"[^a-z0-9 ]", "", name.lower())
    name = re.sub(r"\s+(jr|sr|ii|iii|iv)$", "", name)
    name = name.replace(" ", "")
    return {"kenwalker": "kennethwalker", "hollywoodbrown": "marquisebrown",
            "joshuapalmer": "joshpalmer"}.get(name, name)

def read_stats():
    """Read cleaned statistics and remove the duplicate zero-game Moore row."""
    with (ROOT / 'data/intermediate/NFLData_cleaned.csv').open(encoding='utf-8-sig', newline='') as file:
        rows = list(csv.DictReader(file))
    groups = defaultdict(list)
    for row in rows:
        groups[(normalize_name(row['Player']), row['FantPos'])].append(row)
    result = []
    removed = []
    for key, group in groups.items():
        if len(group) == 1:
            result.extend(group)
        elif key == ('elijahmoore', 'WR') and len(group) == 2:
            keep = [r for r in group if r['Tm'] == 'BUF' and r['G'] == '9']
            drop = [r for r in group if r['Tm'] == 'DEN' and r['G'] == '0']
            assert len(keep) == len(drop) == 1
            result.extend(keep)
            removed.extend(drop)
        else:
            raise ValueError(f'Unresolved duplicate: {key}')
    return result, removed

def read_adp():
    """Restore tabs before wrapped positions and validate all 24 fields."""
    raw = (SOURCE / 'adp.txt').read_text(encoding='utf-8-sig')
    start = re.search(r'(?m)^1\t', raw).start()
    headers = [v.strip() for v in re.split(r'[\t\n]+', raw[:start]) if v.strip()]
    assert len(headers) == 24
    rows = []
    repaired = []
    for block in re.split(r'(?m)(?=^\d+\t)', raw[start:]):
        if not block.strip():
            continue
        block, count = re.subn(r' *\n(?=(?:QB|RB|WR|TE|PK|TD|CB)\d+\t)', '\t', block)
        values = [v.strip() for v in block.strip('\n').split('\t')]
        if len(values) != 24:
            raise ValueError(f'Wrong column count for ADP row {values[0]}: {len(values)}')
        row = dict(zip(headers, values))
        assert re.fullmatch(r'(QB|RB|WR|TE|PK|TD|CB)\d+', row['Consensus Pos'])
        assert re.fullmatch(r'[A-Z]{2,3} /\d+|FA', row['Team/Bye'])
        assert all(v == '-' or v.isdigit() for v in values[4:])
        if count:
            repaired.append(int(row['Consensus']))
        rows.append(row)
    ranks = [int(r['Consensus']) for r in rows]
    assert len(ranks) == len(set(ranks)) == 350
    assert ranks == sorted(ranks)
    return rows, repaired

def number(value):
    """Convert known missing markers to blanks and other values to numbers."""
    if value in ('', '-', None):
        return None
    value = float(value)
    return int(value) if value.is_integer() else value

def merge_key(row, source):
    """Match names and compatible positions without requiring team agreement."""
    position = row['FantPos'] if source == 'stats' else re.sub(r'\d+', '', row['Consensus Pos'])
    if position == 'FB':
        position = 'RB'
    if normalize_name(row['Player']) == 'travishunter' and position == 'CB':
        position = 'WR'
    return normalize_name(row['Player']), position

def main():
    """Merge players, write the submission CSV, and print row counts."""
    stats, removed = read_stats()
    adp_all, repaired = read_adp()
    adp = [r for r in adp_all if not r['Consensus Pos'].startswith(('TD', 'PK'))]
    stats_index = {merge_key(r, 'stats'): r for r in stats}
    adp_index = {merge_key(r, 'adp'): r for r in adp}
    assert len(stats_index) == len(stats)
    assert len(adp_index) == len(adp)
    stat_fields = {'Age': 'age', 'G': 'games_played', 'GS': 'games_started',
                   'FantPt': 'fantasy_points_standard', 'PPR': 'fantasy_points_ppr',
                   'DKPt': 'fantasy_points_draftkings', 'FDPt': 'fantasy_points_fanduel',
                   'VBD': 'stats_value_based_drafting', 'PosRank': 'stats_position_rank',
                   'OvRank': 'stats_overall_rank'}
    platforms = [c for c in list(adp_all[0])[4:] if any(r[c] != '-' for r in adp)]
    platform_fields = {c: 'adp_' + re.sub(r'[^a-z0-9]+', '_', c.lower()).strip('_') + '_rank' for c in platforms}
    result = []
    for key in sorted(stats_index.keys() | adp_index.keys()):
        s, a = stats_index.get(key, {}), adp_index.get(key, {})
        team_bye = a.get('Team/Bye', '').split(' /')
        row = {'player': s.get('Player', a.get('Player')), 'position': key[1],
               'stats_player_name': s.get('Player', ''), 'adp_player_name': a.get('Player', ''),
               'stats_position': s.get('FantPos', ''),
               'adp_position': re.sub(r'\d+', '', a.get('Consensus Pos', '')),
               'stats_team': s.get('Tm', ''), 'adp_team': team_bye[0],
               'adp_bye_week': number(team_bye[1]) if len(team_bye) == 2 else None,
               'match_status': 'matched' if s and a else ('stats_only' if s else 'adp_only')}
        row.update({label: number(s.get(col)) for col, label in stat_fields.items()})
        row['adp_consensus_rank'] = number(a.get('Consensus'))
        row['adp_position_rank'] = number(re.sub(r'\D', '', a.get('Consensus Pos', '')))
        row.update({label: number(a.get(col)) for col, label in platform_fields.items()})
        result.append(row)
    result.sort(key=lambda r: (r['adp_consensus_rank'] is None, r['adp_consensus_rank'] or 0, r['player']))
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open('w', encoding='utf-8-sig', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=list(result[0]))
        writer.writeheader()
        writer.writerows(result)
    counts = Counter(row['match_status'] for row in result)
    print(f'Wrote {len(result)} players and {len(result[0])} columns to {OUTPUT.name}')
    print(f'Repaired ADP rows: {len(repaired)}; removed duplicate rows: {len(removed)}')
    print(dict(counts))


if __name__ == '__main__':
    main()
