import numpy as np

from src.parser.base import NearTargetParser, TargetParser


class C3NearTargetsParser(NearTargetParser):
    lower_color = np.array([109, 0, 242])
    upper_color = np.array([179, 255, 255])


class C3TargetParser(TargetParser):
    x_offset = 0
    y_offset = 0
    w = 0
    h = 0
    lower_color = np.array([109, 0, 242])
    upper_color = np.array([179, 255, 255])
