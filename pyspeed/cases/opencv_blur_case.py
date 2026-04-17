from __future__ import annotations

import cv2
import numpy as np
from PIL import Image, ImageFilter


CASE_NAME = "opencv_blur"
CASE_DESCRIPTION = "Compare OpenCV Gaussian blur with Pillow GaussianBlur on RGB images."

HEIGHT = 1080
WIDTH = 1920
IMAGE = (np.arange(HEIGHT * WIDTH * 3, dtype=np.uint8) % 251).reshape(HEIGHT, WIDTH, 3)
PIL_IMAGE = Image.fromarray(IMAGE)


def baseline() -> int:
    blurred = PIL_IMAGE.filter(ImageFilter.GaussianBlur(radius=1.6))
    result = np.asarray(blurred)
    return int(result[0, 0, 0]) + int(result[-1, -1, -1]) + result.size


def optimized() -> int:
    blurred = cv2.GaussianBlur(IMAGE, (5, 5), 0)
    return int(blurred[0, 0, 0]) + int(blurred[-1, -1, -1]) + blurred.size


def build_functions():
    return baseline, optimized
