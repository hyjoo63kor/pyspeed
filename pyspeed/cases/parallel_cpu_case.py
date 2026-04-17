from __future__ import annotations

import os
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import get_context


CASE_NAME = "parallel"
CASE_DESCRIPTION = "Use multiprocessing instead of threading for CPU-bound work."

WORKER_COUNT = max(2, min(4, os.cpu_count() or 1))
CHUNK_SIZE = 120_000
ROUND_COUNT = 5
CHUNKS = [
    (200_000 + idx * CHUNK_SIZE, 200_000 + (idx + 1) * CHUNK_SIZE)
    for idx in range(WORKER_COUNT)
]


def cpu_heavy_task(bounds: tuple[int, int]) -> int:
    start, end = bounds
    total = 0
    for value in range(start, end):
        current = value
        digit_square_sum = 0
        while current:
            current, remainder = divmod(current, 10)
            digit_square_sum += remainder * remainder
        total += digit_square_sum
    return total


def baseline() -> int:
    total = 0
    for _ in range(ROUND_COUNT):
        with ThreadPoolExecutor(max_workers=WORKER_COUNT) as executor:
            total += sum(executor.map(cpu_heavy_task, CHUNKS))
    return total


def optimized() -> int:
    total = 0
    ctx = get_context("spawn")
    with ctx.Pool(processes=WORKER_COUNT) as pool:
        for _ in range(ROUND_COUNT):
            total += sum(pool.map(cpu_heavy_task, CHUNKS))
    return total


def build_functions():
    return baseline, optimized
