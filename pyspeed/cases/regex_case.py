from __future__ import annotations

import re


CASE_NAME = "regex"
CASE_DESCRIPTION = "Compile regex once instead of rebuilding it for every match."

LINES = [f"user-{idx}@example.com" if idx % 3 else f"bad-address-{idx}" for idx in range(8_000)]
PATTERN_TEXT = r"^[a-z]+-\d+@example\.com$"
PATTERN = re.compile(PATTERN_TEXT)


def baseline() -> int:
    matches = 0
    for line in LINES:
        if re.match(PATTERN_TEXT, line):
            matches += 1
    return matches


def optimized() -> int:
    matches = 0
    match = PATTERN.match
    for line in LINES:
        if match(line):
            matches += 1
    return matches


def build_functions():
    return baseline, optimized
