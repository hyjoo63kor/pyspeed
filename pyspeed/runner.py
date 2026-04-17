from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from importlib import import_module
from time import perf_counter_ns
from timeit import repeat
from typing import Callable


SECONDS_PER_RUN = 5
REPEATS = 3
TIMER_CHOICES = ("timeit", "perf_counter_ns")
PROFILE_CHOICES = ("quick", "full")


@dataclass(frozen=True)
class Case:
    name: str
    description: str
    factory: Callable[[], tuple[Callable[[], object], Callable[[], object]]]


@dataclass(frozen=True)
class Result:
    case: str
    description: str
    timer: str
    baseline_best: float
    optimized_best: float
    speedup: float


@dataclass(frozen=True)
class MeasureConfig:
    number: int
    repeat: int


def _load_case(module_name: str) -> Case:
    module = import_module(f"pyspeed.cases.{module_name}")
    return Case(
        name=module.CASE_NAME,
        description=module.CASE_DESCRIPTION,
        factory=module.build_functions,
    )


CASE_REGISTRY = {
    "loops": ("loops", "Compare repeated function calls with a simpler inlined loop."),
    "strings": ("strings", "Compare repeated string concatenation with ''.join(...)."),
    "lookups": ("lookups", "Reduce repeated global and attribute lookups inside tight loops."),
    "slots": ("slots_case", "Compare regular dataclass instances with slots-enabled dataclasses."),
    "cache": ("cache_case", "Use lru_cache for repeated recursive work."),
    "dictget": ("dictget_case", "Avoid exception-heavy dictionary access in hot loops."),
    "regex": ("regex_case", "Compile regex once instead of rebuilding it for every match."),
    "csv": ("csv_case", "Use csv.reader with fixed column indexes instead of DictReader in hot loops."),
    "opencv_resize": ("opencv_resize_case", "Compare OpenCV resize with Pillow resize for RGB images."),
    "opencv_blur": ("opencv_blur_case", "Compare OpenCV Gaussian blur with Pillow GaussianBlur on RGB images."),
    "ctypes": ("ctypes_case", "Use ctypes.memmove for bulk byte copies instead of Python-level loops."),
    "cdll": ("cdll_case", "Call a compiled C DLL through ctypes for bulk numeric work."),
    "fileio": ("fileio_case", "Buffer text in memory before writing instead of many tiny writes."),
    "normalize": ("normalize_case", "Normalize and encode text once instead of repeating it in hot loops."),
    "parallel": ("parallel_cpu_case", "Use multiprocessing instead of threading for CPU-bound work."),
    "numpy": ("numpy_case", "Use NumPy vectorization instead of Python loops for numeric transforms."),
    "numba": ("numba_case", "Use Numba JIT compilation for hot numeric loops after a warm-up compile."),
    "numba_cold": ("numba_cold_case", "Include Numba compilation overhead to show one-off run cost."),
}


def load_case_by_name(case_name: str) -> Case:
    module_name, _ = CASE_REGISTRY[case_name]
    return _load_case(module_name)


def build_measure_config(profile_name: str, number: int | None, repeat_count: int | None) -> MeasureConfig:
    defaults = {
        "quick": MeasureConfig(number=1, repeat=1),
        "full": MeasureConfig(number=SECONDS_PER_RUN, repeat=REPEATS),
    }
    config = defaults[profile_name]
    return MeasureConfig(
        number=number if number is not None else config.number,
        repeat=repeat_count if repeat_count is not None else config.repeat,
    )


def _measure_timeit(fn: Callable[[], object], config: MeasureConfig) -> list[float]:
    return repeat(fn, repeat=config.repeat, number=config.number)


def _measure_perf_counter_ns(fn: Callable[[], object], config: MeasureConfig) -> list[float]:
    runs: list[float] = []
    for _ in range(config.repeat):
        start = perf_counter_ns()
        for _ in range(config.number):
            fn()
        elapsed_seconds = (perf_counter_ns() - start) / 1_000_000_000
        runs.append(elapsed_seconds)
    return runs


def benchmark(case: Case, timer_name: str = "timeit", config: MeasureConfig | None = None) -> Result:
    baseline, optimized = case.factory()
    config = config or MeasureConfig(number=SECONDS_PER_RUN, repeat=REPEATS)

    if timer_name == "timeit":
        measure = _measure_timeit
    elif timer_name == "perf_counter_ns":
        measure = _measure_perf_counter_ns
    else:
        raise ValueError(f"unsupported timer: {timer_name}")

    baseline_runs = measure(baseline, config)
    optimized_runs = measure(optimized, config)

    baseline_best = min(baseline_runs)
    optimized_best = min(optimized_runs)
    speedup = baseline_best / optimized_best

    return Result(
        case=case.name,
        description=case.description,
        timer=timer_name,
        baseline_best=baseline_best,
        optimized_best=optimized_best,
        speedup=speedup,
    )


def format_result_text(result: Result) -> str:
    lines = [
        f"[{result.case}] {result.description}",
        f"timer         : {result.timer}",
        f"baseline best : {result.baseline_best:.6f}s",
        f"optimized best: {result.optimized_best:.6f}s",
        f"speedup       : {result.speedup:.2f}x",
    ]
    return "\n".join(lines)


def format_results_json(results: list[Result]) -> str:
    payload = [
        {
            "case": result.case,
            "description": result.description,
            "timer": result.timer,
            "baseline_best": result.baseline_best,
            "optimized_best": result.optimized_best,
            "speedup": result.speedup,
        }
        for result in results
    ]
    return json.dumps(payload, indent=2)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run Python speed benchmark examples.")
    parser.add_argument(
        "case",
        nargs="?",
        default="all",
        help="Case name to run, or 'all'",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List available benchmark cases.",
    )
    parser.add_argument(
        "--timer",
        default="timeit",
        choices=TIMER_CHOICES,
        help="Benchmark timer to use.",
    )
    parser.add_argument(
        "--format",
        default="text",
        choices=("text", "json"),
        help="Output format to print.",
    )
    parser.add_argument(
        "--skip-case",
        action="append",
        default=[],
        choices=tuple(CASE_REGISTRY),
        help="Case name to skip. Can be passed multiple times.",
    )
    parser.add_argument(
        "--profile",
        default="full",
        choices=PROFILE_CHOICES,
        help="Measurement profile to use.",
    )
    parser.add_argument(
        "--number",
        type=int,
        help="Override loop count per repeat.",
    )
    parser.add_argument(
        "--repeat-count",
        type=int,
        help="Override repeat count.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.list:
        for case_name, (_, description) in CASE_REGISTRY.items():
            print(f"{case_name:8} {description}")
        return 0

    config = build_measure_config(args.profile, args.number, args.repeat_count)
    selected_case_names = [case_name for case_name in CASE_REGISTRY if case_name not in set(args.skip_case)]

    if args.case == "all":
        results = [
            benchmark(load_case_by_name(case_name), timer_name=args.timer, config=config)
            for case_name in selected_case_names
        ]
        if args.format == "json":
            print(format_results_json(results))
            return 0
        for result in results:
            print(format_result_text(result))
            print()
        return 0

    if args.case not in CASE_REGISTRY:
        parser.error(f"unknown case: {args.case}")
    if args.case in args.skip_case:
        parser.error(f"requested case is also skipped: {args.case}")

    case = load_case_by_name(args.case)
    result = benchmark(case, timer_name=args.timer, config=config)
    if args.format == "json":
        print(format_results_json([result]))
    else:
        print(format_result_text(result))
    return 0
