class PlayerStatus:
    def __init__(self, level, name, is_fishing, is_dead, hp, mp, cp):
        self.name = name
        self.level = level
        self.hp = hp
        self.mp = mp
        self.cp = cp
        self.is_fishing = is_fishing
        self.is_dead = is_dead


class StatusPair:
    def __init__(self, first, second):
        self.first = first
        self.second = second

