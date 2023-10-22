import numpy as np

from src.parser.base import NearTargetParser


class C3NearTargetsParser(NearTargetParser):
    # lower_color = np.array([0, 0, 0])
    # upper_color = np.array([179, 9, 255])

    lower_color = np.array([109, 0, 242])
    upper_color = np.array([179, 255, 255])
