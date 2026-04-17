from __future__ import annotations

import ctypes


CASE_NAME = "ctypes"
CASE_DESCRIPTION = "Use ctypes.memmove for bulk byte copies instead of Python-level loops."

SOURCE_BYTES = bytes((idx * 13) % 251 for idx in range(300_000))
SOURCE_BUFFER = ctypes.create_string_buffer(SOURCE_BYTES)
BUFFER_SIZE = len(SOURCE_BYTES)


def baseline() -> int:
    destination = bytearray(BUFFER_SIZE)
    for index, value in enumerate(SOURCE_BYTES):
        destination[index] = value
    return destination[0] + destination[-1] + len(destination)


def optimized() -> int:
    destination = (ctypes.c_ubyte * BUFFER_SIZE)()
    ctypes.memmove(destination, SOURCE_BUFFER, BUFFER_SIZE)
    return destination[0] + destination[BUFFER_SIZE - 1] + BUFFER_SIZE


def build_functions():
    return baseline, optimized
