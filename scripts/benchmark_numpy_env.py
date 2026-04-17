from __future__ import annotations

import json
import platform
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from time import perf_counter
from typing import Callable

import numpy as np


RESULTS_PATH = Path("results/numpy_env_benchmark.json")
TEXT_PATH = Path("results/numpy_env_benchmark.txt")
REPEATS = 3


@dataclass(frozen=True)
class BenchResult:
    name: str
    best_seconds: float


def measure(name: str, fn: Callable[[], object], repeats: int = REPEATS) -> BenchResult:
    runs: list[float] = []
    for _ in range(repeats):
        start = perf_counter()
        fn()
        runs.append(perf_counter() - start)
    return BenchResult(name=name, best_seconds=min(runs))


def format_text(payload: dict) -> str:
    lines = [
        f"generated_at    : {payload['generated_at']}",
        f"python_version  : {payload['python_version']}",
        f"numpy_version   : {payload['numpy_version']}",
        f"platform        : {payload['platform']}",
        f"blas            : {payload['blas']}",
        f"simd_found      : {', '.join(payload['simd_found']) or '-'}",
        "",
        "benchmarks:",
    ]
    for item in payload["benchmarks"]:
        lines.append(f"  {item['name']:18} {item['best_seconds']:.6f}s")
    return "\n".join(lines)


def main() -> int:
    rng = np.random.default_rng(42)
    values = rng.random(400_000, dtype=np.float64)
    lhs = rng.random((250, 250), dtype=np.float64)
    rhs = rng.random((250, 250), dtype=np.float64)

    config = np.__config__.CONFIG
    blas_name = config.get("Build Dependencies", {}).get("blas", {}).get("name", "unknown")
    simd_found = config.get("SIMD Extensions", {}).get("found", [])

    benchmarks = [
        measure("vector_transform", lambda: ((values * values * 1.5) + (values / 3.0) - 7.0).sum()),
        measure("dot_product", lambda: np.dot(values, values)),
        measure("matrix_multiply", lambda: lhs @ rhs),
        measure("sort", lambda: np.sort(values)),
    ]

    payload = {
        "generated_at": __import__("datetime").datetime.now().isoformat(timespec="seconds"),
        "python_version": platform.python_version(),
        "numpy_version": np.__version__,
        "platform": platform.platform(),
        "blas": blas_name,
        "simd_found": simd_found,
        "benchmarks": [asdict(item) for item in benchmarks],
    }

    RESULTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    RESULTS_PATH.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    TEXT_PATH.write_text(format_text(payload), encoding="utf-8")
    print(format_text(payload))
    print("")
    print(f"Saved JSON to {RESULTS_PATH}")
    print(f"Saved text to {TEXT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
