from __future__ import annotations

import unicodedata


CASE_NAME = "normalize"
CASE_DESCRIPTION = "Normalize and encode text once instead of repeating it in hot loops."

PHRASES = [
    "Cafe\u0301 au lait",
    "na\u00efve approach",
    "re\u0301sume\u0301 draft",
    "S\u00e3o Paulo",
    "pi\u00f1ata party",
    "coo\u0308perate fully",
    "smile \U0001F642",
] * 600
NORMALIZED_BYTES = [unicodedata.normalize("NFC", phrase).encode("utf-8") for phrase in PHRASES]


def baseline() -> int:
    total = 0
    for phrase in PHRASES:
        total += len(unicodedata.normalize("NFC", phrase).encode("utf-8"))
    return total


def optimized() -> int:
    return sum(len(item) for item in NORMALIZED_BYTES)


def build_functions():
    return baseline, optimized
