class FishingResult:
    is_fishing = False
    seconds_left = None
    hp_percent = None


class NearTargetResult:
    def __init__(self, x, y, name, distance):
        self.x = x
        self.y = y
        self.name = name
        self.distance = distance
