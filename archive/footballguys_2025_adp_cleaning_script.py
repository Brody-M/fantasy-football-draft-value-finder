from pathlib import Path
import csv
import re

source = Path("adp.txt")
output = Path("footballguys_2025_adp_cleaned.csv")

raw = source.read_text(encoding="utf-8", errors="replace").replace("\r\n", "\n").replace("\r", "\n")
header_end = raw.find("\n1\t")
if header_end < 0:
    raise ValueError("Could not find the first ADP row.")

headers = [value.strip() for value in raw[:header_end].split("\n") if value.strip()]
expected_columns = len(headers)
rows = []
problems = []

for block in re.split(r"(?m)(?=^\d+\t)", raw[header_end + 1:]):
    if not block.strip():
        continue
    rank, rest = block.split("\t", 1)
    row = [rank] + [re.sub(r"\s+", " ", value).strip() for value in rest.replace("\n", " ").split("\t")]
    if len(row) != expected_columns:
        problems.append((rank, len(row)))
        continue
    rows.append(row)

if problems:
    raise ValueError(f"Stopped without writing a modified file. Rows with the wrong column count: {problems}")

with output.open("w", newline="", encoding="utf-8-sig") as file:
    writer = csv.writer(file)
    writer.writerow(headers)
    writer.writerows(rows)

print(f"Wrote {len(rows)} rows to {output}")