import numpy as np

from src.parser.base import NearTargetsParser, TargetParser, UserStatusParser


class ClassicNearTargetsParser(NearTargetsParser):
    lower_color = np.array([0, 0, 0])
    upper_color = np.array([0, 0, 255])


class ClassicTargetParser(TargetParser):
    x_offset = 19
    y_offset = 25
    w = 145
    h = 5

    lower_color = np.array([0, 145, 153])
    upper_color = np.array([179, 255, 255])


class ClassicUserStatusParser(UserStatusParser):
    cp_x_offset = 25
    cp_y_offset = -2
    cp_h = 12
    cp_w = 100

    hp_x_offset = 25
    hp_y_offset = 11
    hp_h = 12
    hp_w = 100

    mp_x_offset = 25
    mp_y_offset = 24
    mp_h = 12
    mp_w = 100

    lower_color = np.array([0, 0, 0])
    upper_color = np.array([179, 38, 255])
