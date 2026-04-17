from __future__ import annotations

import numpy as np


CASE_NAME = "numpy"
CASE_DESCRIPTION = "Use NumPy vectorization instead of Python loops for numeric transforms."

VALUES_LIST = [float(idx) / 100.0 for idx in range(200_000)]
VALUES_ARRAY = np.array(VALUES_LIST, dtype=np.float64)


def baseline() -> float:
    total = 0.0
    for value in VALUES_LIST:
        total += (value * value * 1.5) + (value / 3.0) - 7.0
    return total


def optimized() -> float:
    transformed = (VALUES_ARRAY * VALUES_ARRAY * 1.5) + (VALUES_ARRAY / 3.0) - 7.0
    return float(transformed.sum())


def build_functions():
    return baseline, optimized
