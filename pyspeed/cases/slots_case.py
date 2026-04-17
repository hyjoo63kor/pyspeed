from __future__ import annotations

from dataclasses import dataclass


CASE_NAME = "slots"
CASE_DESCRIPTION = "Compare regular dataclass instances with slots-enabled dataclasses."


@dataclass
class PlainPoint:
    x: int
    y: int
    z: int


@dataclass(slots=True)
class SlottedPoint:
    x: int
    y: int
    z: int


def baseline() -> int:
    total = 0
    for idx in range(40_000):
        point = PlainPoint(idx, idx + 1, idx + 2)
        total += point.x + point.y + point.z
    return total


def optimized() -> int:
    total = 0
    for idx in range(40_000):
        point = SlottedPoint(idx, idx + 1, idx + 2)
        total += point.x + point.y + point.z
    return total


def build_functions():
    return baseline, optimized
