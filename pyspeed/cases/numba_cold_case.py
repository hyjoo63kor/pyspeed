from __future__ import annotations

import numba as nb
import numpy as np


CASE_NAME = "numba_cold"
CASE_DESCRIPTION = "Include Numba compilation overhead to show one-off run cost."

VALUES = np.linspace(0.0, 2_000.0, 200_000, dtype=np.float64)


def python_transform(values: np.ndarray) -> float:
    total = 0.0
    for value in values:
        total += (value * value * 1.5) + (value / 3.0) - 7.0
    return total


def baseline() -> float:
    return python_transform(VALUES)


def optimized() -> float:
    @nb.njit
    def compiled_transform(values: np.ndarray) -> float:
        total = 0.0
        for value in values:
            total += (value * value * 1.5) + (value / 3.0) - 7.0
        return total

    return compiled_transform(VALUES)


def build_functions():
    return baseline, optimized
