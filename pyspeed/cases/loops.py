from __future__ import annotations


CASE_NAME = "loops"
CASE_DESCRIPTION = "Compare repeated function calls with a simpler inlined loop."

DATA = list(range(10_000))


def transform(value: int) -> int:
    return (value * value) - value + 3


def baseline() -> int:
    total = 0
    for value in DATA:
        total += transform(value)
    return total


def optimized() -> int:
    return sum((value * value) - value + 3 for value in DATA)


def build_functions():
    return baseline, optimized
