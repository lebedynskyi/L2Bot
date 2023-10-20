import numpy as np

from app.parser.base import NearTargetParser


class C3NearTargetsParser(NearTargetParser):
    # Color segmentation
    lower_color = np.array([0, 0, 0])
    upper_color = np.array([179, 9, 255])