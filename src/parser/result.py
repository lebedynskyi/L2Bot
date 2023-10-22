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
