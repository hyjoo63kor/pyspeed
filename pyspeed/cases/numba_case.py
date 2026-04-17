from __future__ import annotations

import numba as nb
import numpy as np


CASE_NAME = "numba"
CASE_DESCRIPTION = "Use Numba JIT compilation for hot numeric loops after a warm-up compile."

VALUES = np.linspace(0.0, 2_000.0, 200_000, dtype=np.float64)


def python_transform(values: np.ndarray) -> float:
    total = 0.0
    for value in values:
        total += (value * value * 1.5) + (value / 3.0) - 7.0
    return total


@nb.njit
def numba_transform(values: np.ndarray) -> float:
    total = 0.0
    for value in values:
        total += (value * value * 1.5) + (value / 3.0) - 7.0
    return total


def baseline() -> float:
    return python_transform(VALUES)


def optimized() -> float:
    return numba_transform(VALUES)


def build_functions():
    numba_transform(VALUES)
    return baseline, optimized
