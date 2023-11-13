class FishingResult:
    is_fishing = False
    seconds_left = None
    hp_percent = None


class NearTargetResult:
    def __init__(self, x, y, w, h, name, distance):
        self.h = h
        self.w = w
        self.x = x
        self.y = y
        self.name = name
        self.distance = distance


class TargetResult:
    exist = False
    hp = 0


class UserStatusResult:
    hp = 0
    mp = 0
    cp = 0
