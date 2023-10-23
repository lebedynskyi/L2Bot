import logging
import time

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
        y = target.y + self.capture.offset_y + (target.h / 2) + 12
        self.keyboard.mouse_click(self.keyboard.KEY_MOUSE_LEFT, (x, y))

    def cancel(self):
        self.keyboard.esc()


class HandlerSpoilerAutoFarm(BaseHandler):
    STATE_SPOIL = 2
    STATE_MANOR = 3
    logger = logging.getLogger("SpoilerAutoFarm")
    after_kill = False
    target_counter = 0

    def __init__(self, controller: ControllerSpoilerAutoFarm,
                 near_target_parser: NearTargetParser,
                 target_parser: TargetParser, *mobs):
        self.target_parser = target_parser
        self.near_target_parser = near_target_parser
        self.controller = controller
        self.mobs = mobs

    def _on_tick(self, screen_rgb, screen_gray, delta):
        # Add parsing of name
        target = self.target_parser.parse(screen_rgb, screen_gray)
        if self.state == STATE_IDLE:
            self.logger.info("State IDLE. LOOK for target")
            if target.exist:
                self.logger.info("State IDLE. target already exist. Aggr or target already found")
                self.controller.spoil()
                self.target_counter = 0
                self.state = self.STATE_SPOIL
                return True

            # TODO skip killed monster. It is nearest. Need to adjust logic to skip nearest? After spoil it disappear
            target = self._find_target(screen_rgb, screen_gray)
            if self.target_counter >= 3:
                # Bot got stuck. Not able to select target in move
                self.target_counter = 0
                self.logger.warning("Bot got stuck. Wait a little")
                time.sleep(3)
                return True

            if target is not None:
                self.controller.select_target(target)
                self.logger.info("State IDLE. Target selected by mouse, distance %s", target.distance)
                self.target_counter = self.target_counter + 1
                time.sleep(0.2)
                self.target_counter = 0
                self.controller.spoil()
                self.state = self.STATE_SPOIL
                return True
            else:
                self.controller.next_target()
                time.sleep(0.2)
                self.controller.spoil()
                self.target_counter = 0
                self.logger.info("State IDLE. Target selected by command")
                self.state = self.STATE_SPOIL
                return True

        # TODO Add timer to reset target and sleect via target
        if self.state == self.STATE_SPOIL:
            if not target.exist:
                self.logger.warning("State SPOIL, Target not exist. Reset state")
                self._reset()
                return True

            # TODO 1 time action
            if target.hp <= 50:
                self.controller.manor()
                self.state = self.STATE_MANOR
                return True

            if delta > 6 and target.hp > 90:
                self.logger.info("State SPOIL, Probably got stuck. Select another target by command")
                self.controller.cancel()
                self._reset()
                return True

            self.logger.info("State SPOIL, Keep fighting. Target hp %s", target.hp)

        if self.state == self.STATE_MANOR:
            if not target.exist:
                self.logger.warning("State MANOR, Target not exist. Reset state")
                self._reset()
                return True

            if target.hp == 0:
                self.logger.info("Tared killed. Sweep / Harvest")
                self.controller.sweep()
                time.sleep(0.2)
                self.controller.harvest()
                time.sleep(0.2)
                self.controller.pick_up()
                time.sleep(0.2)
                self.controller.pick_up()
                time.sleep(0.2)
                self.controller.cancel()
                self.state = STATE_IDLE
                self.after_kill = True
                return True

            self.logger.info("State MANOR, Keep fighting. Target hp %s", target.hp)
        return False

    def _reset(self):
        self.controller.cancel()
        self.after_kill = False
        self.state = STATE_IDLE

    def _find_target(self, screen_rgb, screen_gray):
        targets = self.near_target_parser.parse(screen_rgb, screen_gray)
        interested_mobs = []
        for target in targets:
            for mob in self.mobs:
                if fuzz.ratio(target.name, mob) >= 65:
                    interested_mobs.append(target)

        if interested_mobs:
            if self.after_kill and len(interested_mobs) > 1:
                if interested_mobs[0].distance > 50:
                    return interested_mobs[0]

                return interested_mobs[1]
            else:
                return interested_mobs[0]
