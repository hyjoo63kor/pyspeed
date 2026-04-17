from __future__ import annotations

from pathlib import Path
from uuid import uuid4


CASE_NAME = "fileio"
CASE_DESCRIPTION = "Buffer text in memory before writing instead of many tiny writes."

LINES = [f"row-{idx}\n" for idx in range(5_000)]
RESULTS_DIR = Path("results") / "fileio-temp"


def _target_path(prefix: str) -> Path:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    return RESULTS_DIR / f"{prefix}-{uuid4().hex}.txt"


def baseline() -> int:
    path = _target_path("baseline")
    with path.open("w", encoding="utf-8") as handle:
        for line in LINES:
            handle.write(line)
    return path.stat().st_size


def optimized() -> int:
    path = _target_path("optimized")
    path.write_text("".join(LINES), encoding="utf-8")
    return path.stat().st_size


def build_functions():
    return baseline, optimized
