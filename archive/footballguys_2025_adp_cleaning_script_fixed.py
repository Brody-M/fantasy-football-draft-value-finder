from pathlib import Path
import csv
import re

source = Path("adp.txt")
output = Path("footballguys_2025_adp_cleaned.csv")

raw = source.read_text(encoding="utf-8", errors="replace")
raw = raw.replace("\r\n", "\n").replace("\r", "\n")

header_end = raw.find("\n1\t")
if header_end == -1:
    raise ValueError("Could not locate the first data row.")

headers = [
    "Consensus",
    "Player",
    "Consensus Pos",
    "Team/Bye",
    "BestBall10s",
    "CBS",
    "DraftKings",
    "Drafters",
    "ESPN",
    "FBG OC",
    "FFPC",
    "MFL",
    "NFFC",
    "RT Sports",
    "Sleeper 1QB",
    "Sleeper 1QB Rookie",
    "Sleeper IDP",
    "Sleeper IDP SF",
    "Sleeper Redraft",
    "Sleeper SF",
    "Sleeper SF Redraft",
    "Sleeper SF Rookie",
    "Underdog",
    "Yahoo!"
]

rows = []
blocks = re.split(r"(?m)(?=^\d+\t)", raw[header_end + 1:])

for block in blocks:
    if not block.strip():
        continue

    rank, remaining = block.split("\t", 1)

    fields = [
        re.sub(r"\s+", " ", value).strip()
        for value in remaining.replace("\n", " ").split("\t")
    ]

    row = [rank] + fields

    # The source has rows that omit only trailing blank fields.
    # Pad those blanks so every CSV row has the same 24 columns.
    if len(row) < len(headers):
        row.extend([""] * (len(headers) - len(row)))

    if len(row) != len(headers):
        raise ValueError(
            f"Row {rank} has {len(row)} columns; expected {len(headers)}. "
            "No CSV was written."
        )

    rows.append(row)

with output.open("w", newline="", encoding="utf-8-sig") as file:
    writer = csv.writer(file)
    writer.writerow(headers)
    writer.writerows(rows)

print(f"Success: wrote {len(rows)} rows to {output.resolve()}")