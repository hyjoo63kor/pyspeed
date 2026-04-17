from __future__ import annotations

import cv2
import numpy as np
from PIL import Image


CASE_NAME = "opencv_resize"
CASE_DESCRIPTION = "Compare OpenCV resize with Pillow resize for RGB images."

HEIGHT = 1080
WIDTH = 1920
TARGET_SIZE = (640, 360)
IMAGE = (np.arange(HEIGHT * WIDTH * 3, dtype=np.uint8) % 251).reshape(HEIGHT, WIDTH, 3)
PIL_IMAGE = Image.fromarray(IMAGE, mode="RGB")


def baseline() -> int:
    resized = PIL_IMAGE.resize(TARGET_SIZE, Image.Resampling.BILINEAR)
    result = np.asarray(resized)
    return int(result[0, 0, 0]) + int(result[-1, -1, -1]) + result.size


def optimized() -> int:
    resized = cv2.resize(IMAGE, TARGET_SIZE, interpolation=cv2.INTER_LINEAR)
    return int(resized[0, 0, 0]) + int(resized[-1, -1, -1]) + resized.size


def build_functions():
    return baseline, optimized
