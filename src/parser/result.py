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
    hp = (0, 0)
    mp = (0, 0)
    cp = (0, 0)


class ResultSquare:
    def __init__(self, x, y, h, w):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def middle(self):
        return self.x + self.w / 2, self.y + self.h / 2


class ManorWindowResult:
    def __init__(self, exist: bool = False, sell_crop_btn: ResultSquare = None):
        self.exist = exist
        self.sell_crop_btn = sell_crop_btn


class ManorWindowCropListResult:
    def __init__(self, exist: bool = False, sell_crop_btn: ResultSquare = None,
                 first_crop_item: ResultSquare = None, second_crop_item: ResultSquare = None):
        self.second_crop_item = second_crop_item
        self.first_crop_item = first_crop_item
        self.sell_crop_btn = sell_crop_btn
        self.exist = exist


class ManorWindowPriceListResult:

    def __init__(self, exist=False, chooser_btn: ResultSquare = None,
                 max_price_btn: ResultSquare = None, ok_btn: ResultSquare = None, first_crop_item: ResultSquare = None,
                 second_crop_item: ResultSquare = None, third_crop_item: ResultSquare = None,
                 fourth_crop_item: ResultSquare = None):
        self.third_crop_item = third_crop_item
        self.fourth_crop_item = fourth_crop_item
        self.second_crop_item = second_crop_item
        self.first_crop_item = first_crop_item
        self.chooser_btn = chooser_btn
        self.max_price_btn = max_price_btn
        self.ok_btn = ok_btn
        self.exist = exist
