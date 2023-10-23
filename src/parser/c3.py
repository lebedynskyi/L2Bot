import numpy as np

from src.parser.base import NearTargetParser, TargetParser


class C3NearTargetsParser(NearTargetParser):
    lower_color = np.array([109, 0, 242])
    upper_color = np.array([179, 255, 255])


class C3TargetParser(TargetParser):
    x_offset = 16
    y_offset = 26
    w = 150
    h = 5

    lower_color = np.array([0, 145, 153])
    upper_color = np.array([179, 255, 255])
