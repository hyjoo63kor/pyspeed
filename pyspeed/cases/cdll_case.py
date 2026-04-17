from __future__ import annotations

import ctypes
import os
from pathlib import Path

import numpy as np


CASE_NAME = "cdll"
CASE_DESCRIPTION = "Call a compiled C DLL through ctypes for bulk numeric work."

VALUES = np.linspace(0.0, 2_000.0, 200_000, dtype=np.float64)
DEFAULT_DLL_PATH = Path("native") / "build" / "pyspeed_native.dll"


def python_transform(values: np.ndarray) -> float:
    total = 0.0
    for value in values:
        total += (value * value * 1.5) + (value / 3.0) - 7.0
    return total


def load_library() -> ctypes.CDLL:
    dll_path = Path(os.environ.get("PYSPEED_NATIVE_DLL", str(DEFAULT_DLL_PATH)))
    if not dll_path.exists():
        raise RuntimeError(
            f"Native DLL not found: {dll_path}. Build it first with .\\scripts\\build_native.ps1"
        )
    library = ctypes.CDLL(str(dll_path.resolve()))
    library.transform_sum.argtypes = [
        np.ctypeslib.ndpointer(dtype=np.float64, ndim=1, flags=("C_CONTIGUOUS",)),
        ctypes.c_size_t,
    ]
    library.transform_sum.restype = ctypes.c_double
    return library


def baseline() -> float:
    return python_transform(VALUES)


def optimized() -> float:
    library = load_library()
    return float(library.transform_sum(VALUES, VALUES.size))


def build_functions():
    load_library()
    return baseline, optimized
