from __future__ import annotations


CASE_NAME = "strings"
CASE_DESCRIPTION = "Compare repeated string concatenation with ''.join(...)."

PARTS = [f"item-{idx}" for idx in range(3_000)]


def baseline() -> str:
    text = ""
    for part in PARTS:
        text += part
    return text


def optimized() -> str:
    return "".join(PARTS)


def build_functions():
    return baseline, optimized
