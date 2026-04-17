from __future__ import annotations


CASE_NAME = "dictget"
CASE_DESCRIPTION = "Avoid exception-heavy dictionary access in hot loops."

COUNTS = {str(idx): idx for idx in range(2_000)}
KEYS = [str(idx % 2_500) for idx in range(20_000)]


def baseline() -> int:
    total = 0
    for key in KEYS:
        try:
            total += COUNTS[key]
        except KeyError:
            total += 0
    return total


def optimized() -> int:
    total = 0
    get = COUNTS.get
    for key in KEYS:
        total += get(key, 0)
    return total


def build_functions():
    return baseline, optimized
