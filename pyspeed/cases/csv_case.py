from __future__ import annotations

import csv
from io import StringIO


CASE_NAME = "csv"
CASE_DESCRIPTION = "Use csv.reader with fixed column indexes instead of DictReader in hot loops."

ROWS = ["name,score,count"]
for idx in range(4_000):
    ROWS.append(f"user-{idx},{idx % 100},{(idx * 3) % 17}")
CSV_TEXT = "\n".join(ROWS)


def baseline() -> int:
    total = 0
    reader = csv.DictReader(StringIO(CSV_TEXT))
    for row in reader:
        total += int(row["score"]) + int(row["count"])
    return total


def optimized() -> int:
    total = 0
    reader = csv.reader(StringIO(CSV_TEXT))
    next(reader)
    for row in reader:
        total += int(row[1]) + int(row[2])
    return total


def build_functions():
    return baseline, optimized
