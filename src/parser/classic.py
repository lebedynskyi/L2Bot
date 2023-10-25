import cv2
import numpy as np

from src.ocr.recognition import NumbersRecognition
from src.parser.base import BaseParser, NearTargetParser, TargetParser
from src.parser.result import FishingResult
from src.template import GraciaRebornTemplates


class ClassicNearTargetsParser(NearTargetParser):
    lower_color = np.array([0, 0, 0])
    upper_color = np.array([0, 49, 255])


class ClassicTargetParser(TargetParser):
    x_offset = 19
    y_offset = 25
    w = 145
    h = 5

    lower_color = np.array([0, 145, 153])
    upper_color = np.array([179, 255, 255])
