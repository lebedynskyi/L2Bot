import logging
import random
import time

from fuzzywuzzy import fuzz

from src.bot.base import BaseHandler, STATE_IDLE
from src.win_capture import Capture
from src.controller import BaseController
from src.keyboard import BaseKeyboard
from src.parser.base import NearTargetParser, TargetParser


# todo need to click near mob title to start moving with pathfinding
class ControllerSpoilerAutoFarm(BaseController):
    def __init__(self, keyboard: BaseKeyboard, capture: Capture):
        super().__init__(keyboard)
        self.capture = capture

    def spoil(self):
        self.keyboard.f1()

    def sweep(self):
        self.keyboard.f2()

    def next_target(self, target):
        if target is not None:
            self.keyboard.text("/target %s" % target)
        else:
            self.keyboard.text("/targetnext")
        time.sleep(0.5)
        self.keyboard.enter()
        pass

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

    def move(self, x, y):
        x = x + self.capture.offset_x
        y = y + self.capture.offset_y
        self.keyboard.mouse_click(self.keyboard.KEY_MOUSE_LEFT, (x, y))

    def cancel(self):
        self.keyboard.esc()


class HandlerSpoilerAutoFarm(BaseHandler):
    STATE_START_FIGHT = 2
    STATE_FIGHT = 3
    logger = logging.getLogger("SpoilerAutoFarm")
    after_kill = False
    random_choice = False
    target_counter = 0

    def __init__(self, controller: ControllerSpoilerAutoFarm,
                 near_target_parser: NearTargetParser,
                 target_parser: TargetParser, mobs=[]):
        self.target_parser = target_parser
        self.near_target_parser = near_target_parser
        self.controller = controller
        self.mobs = mobs

    def _on_tick(self, screen_rgb, screen_gray, delta):
        # Add parsing of name
        target = self.target_parser.parse(screen_rgb, screen_gray)

        if self.state == STATE_IDLE:
            return self._handle_state_idle(screen_rgb, screen_gray, target)

        if self.state == self.STATE_START_FIGHT:
            return self._handle_state_spoil(screen_rgb, screen_gray, target, delta
                                            )
        if self.state == self.STATE_FIGHT:
            return self._handle_state_manor(screen_rgb, screen_gray, target, delta)

        return False

    def _handle_state_idle(self, screen_rgb, screen_gray, target):
        if target.exist:
            self.logger.info("State IDLE. Target exist. Agr or target found.")
            self.controller.spoil()
            self.target_counter = 0
            self.state = self.STATE_START_FIGHT
            return True

        target = self._find_target(screen_rgb, screen_gray, self.random_choice)
        if self.target_counter >= 2:
            self.logger.warning("Cannot select target by mouse. Stop and retry")
            self.target_counter = 0
            self.controller.move(screen_rgb.shape[1] / 2, screen_rgb.shape[0] / 2)
            time.sleep(0.2)
            return True

        if target is not None:
            self.controller.select_target(target)
            self.logger.info("State IDLE. Target selected by mouse, distance %s", target.distance)
            self.target_counter = self.target_counter + 1
            time.sleep(0.2)
            self.controller.spoil()
            return True
        else:
            if self.mobs:
                self.controller.next_target(random.choice(self.mobs))
            else:
                self.controller.next_target(None)
            time.sleep(0.2)
            self.controller.spoil()
            self.target_counter = 0
            self.logger.info("State IDLE. Target selected by command")
            return True

    def _handle_state_spoil(self, screen_rgb, screen_gray, target, delta):
        # TODO Add timer to reset target and select via target
        if not target.exist:
            self.logger.warning("State SPOIL, Target not exist. Reset state")
            self._reset()
            return True

        # TODO 1 time action
        if target.hp <= 50:
            self.controller.manor()
            self.state = self.STATE_FIGHT
            return True

        if delta > 6 and target.hp > 90:
            self.logger.info("State SPOIL, Probably got stuck. Reset state")
            self._reset()
            return True

        self.logger.info("State SPOIL, Keep fighting. Target hp %s", target.hp)
        return False

    def _handle_state_manor(self, screen_rgb, screen_gray, target, delta):
        if not target.exist:
            self.logger.warning("State MANOR, Target not exist. Reset state")
            self._reset()
            return True

        if target.hp == 0:
            self.logger.info("Target killed. Sweep / Harvest")
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
            self.random_choice = False
            return True

        self.logger.info("State MANOR, Keep fighting. Target hp %s", target.hp)
        return False

    def _reset(self):
        self.controller.cancel()
        self.after_kill = False
        self.state = STATE_IDLE
        self.random_choice = True

    def _find_target(self, screen_rgb, screen_gray, random_choice=False):
        targets = self.near_target_parser.parse(screen_rgb, screen_gray)
        interested_mobs = []
        for target in targets:
            for mob in self.mobs:
                if fuzz.ratio(target.name, mob) >= 75:
                    interested_mobs.append(target)

        if interested_mobs:
            if random_choice:
                return random.choice(interested_mobs)

            if self.after_kill and len(interested_mobs) > 1:
                if interested_mobs[0].distance > 60:
                    return interested_mobs[0]

                return interested_mobs[1]
            else:
                return interested_mobs[0]
