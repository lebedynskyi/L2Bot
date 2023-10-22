from fuzzywuzzy import fuzz

from src.bot.base import BaseHandler, STATE_IDLE
from src.capture import Capture
from src.controller import BaseController
from src.keyboard import BaseKeyboard
from src.parser.base import NearTargetParser


class ControllerSpoilerAutoFarm(BaseController):
    def __int__(self, keyboard: BaseKeyboard,  capture: Capture):
        self.keyboard = keyboard
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
        self.keyboard.mouse_move(target.x, target.y)


class HandlerSpoilerAutoFarm(BaseHandler):
    def __init__(self, controller: ControllerSpoilerAutoFarm, near_target_parser: NearTargetParser, *mobs):
        self.near_target_parser = near_target_parser
        self.controller = controller
        self.mobs = mobs

    def _on_tick(self, screen_rgb, screen_gray, time, delta):
        if self.state == STATE_IDLE:
            # TODO check has target. Already found or aggro mob. Need fight
            target = self._find_target(screen_rgb, screen_gray)
            if target is not None:
                self.controller.select_target(target)
            else:
                # TODO we can even use /target command
                self.controller.next_target()
            return True

        return False

    def _find_target(self, screen_rgb, screen_gray):
        targets = self.near_target_parser.parse(screen_rgb, screen_gray)
        interested_mobs = []
        for target in targets:
            for mob in self.mobs:
                if fuzz.ratio(target.name, mob) >= 85:
                    interested_mobs.append(target)

        if interested_mobs:
            return interested_mobs[0]

        # TODO next target
