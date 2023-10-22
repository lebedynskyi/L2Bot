from fuzzywuzzy import fuzz

from src.bot.base import BaseHandler, STATE_IDLE
from src.capture import Capture
from src.controller import BaseController
from src.keyboard import BaseKeyboard
from src.parser.base import NearTargetParser, TargetParser


class ControllerSpoilerAutoFarm(BaseController):
    def __init__(self, keyboard: BaseKeyboard, capture: Capture):
        super().__init__(keyboard)
        self.capture = capture

    def spoil(self):
        self.keyboard.f1()

    def sweep(self):
        self.keyboard.f2()

    def next_target(self):
        self.keyboard.f3()

    def pick_up(self):
        self.keyboard.f4()

    def manor(self):
        self.keyboard.f5()

    def harvest(self):
        self.keyboard.f6()

    def select_target(self, target):
        x = target.x + self.capture.offset_x + (target.w / 2)
        y = target.y + self.capture.offset_y + (target.h / 2) + 10
        self.keyboard.mouse_click(self.keyboard.KEY_MOUSE_LEFT, (x, y))


class HandlerSpoilerAutoFarm(BaseHandler):
    STATE_SPOIL = 1

    def __init__(self, controller: ControllerSpoilerAutoFarm,
                 near_target_parser: NearTargetParser,
                 target_parser: TargetParser, *mobs):
        self.target_parser = target_parser
        self.near_target_parser = near_target_parser
        self.controller = controller
        self.mobs = mobs

    def _on_tick(self, screen_rgb, screen_gray, time, delta):
        if self.state == STATE_IDLE:
            target = self.target_parser.parse(screen_rgb, screen_gray)
            if target.exist:
                self.state = self.STATE_SPOIL
                self.controller.spoil()
                return True

            # TODO skip killed monster. It is nearest. Need to adjust logic to skip nearest? After spoil it disappear
            target = self._find_target(screen_rgb, screen_gray)
            if target is not None:
                self.controller.select_target(target)
                return True
            else:
                self.controller.next_target()
                return True

        return False

    def _find_target(self, screen_rgb, screen_gray):
        targets = self.near_target_parser.parse(screen_rgb, screen_gray)
        interested_mobs = []
        for target in targets:
            for mob in self.mobs:
                if fuzz.ratio(target.name, mob) >= 60:
                    interested_mobs.append(target)

        if interested_mobs:
            return interested_mobs[0]

        # TODO next target