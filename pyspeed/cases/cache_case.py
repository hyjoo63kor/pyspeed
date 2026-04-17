from __future__ import annotations

from functools import lru_cache


CASE_NAME = "cache"
CASE_DESCRIPTION = "Use lru_cache for repeated recursive work."

VALUES = [28, 29, 30, 31, 32, 31, 30, 29, 28] * 2


def fib_plain(n: int) -> int:
    if n < 2:
        return n
    return fib_plain(n - 1) + fib_plain(n - 2)


@lru_cache(maxsize=None)
def fib_cached(n: int) -> int:
    if n < 2:
        return n
    return fib_cached(n - 1) + fib_cached(n - 2)


def baseline() -> int:
    return sum(fib_plain(value) for value in VALUES)


def optimized() -> int:
    fib_cached.cache_clear()
    return sum(fib_cached(value) for value in VALUES)


def build_functions():
    return baseline, optimized
