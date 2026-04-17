from __future__ import annotations


CASE_NAME = "lookups"
CASE_DESCRIPTION = "Reduce repeated global and attribute lookups inside tight loops."

DATA = [str(idx) for idx in range(8_000)]


class Counter:
    def __init__(self) -> None:
        self.total = 0

    def add(self, value: int) -> None:
        self.total += value


def baseline() -> int:
    counter = Counter()
    for item in DATA:
        counter.add(len(item))
    return counter.total


def optimized() -> int:
    counter = Counter()
    add = counter.add
    local_len = len
    for item in DATA:
        add(local_len(item))
    return counter.total


def build_functions():
    return baseline, optimized
