import logging
import random
import time

from fuzzywuzzy import fuzz

from src.bot.base import BaseHandler, STATE_IDLE
from src.controller import BaseController
from src.keyboard import BaseKeyboard
from src.parser.base import NearTargetParser, TargetParser
from src.win_capture import Capture


# todo need to click near mob title to start moving with pathfinding
class ControllerSpoilerAutoFarm(BaseController):
    def __init__(self, keyboard: BaseKeyboard, capture: Capture):
        super().__init__(keyboard)
        self.capture = capture

    def attack(self):
        self.keyboard.f1()

    def spoil(self):
        self.keyboard.f2()

    def sweep(self):
        self.keyboard.f3()

    def pick_up(self):
        self.keyboard.f4()

    def manor(self):
        self.keyboard.f5()

    def harvest(self):
        self.keyboard.f6()

    def cancel(self):
        self.keyboard.esc()

    def next_target(self, target):
        if target is not None:
            self.keyboard.text("/target %s" % target)
        else:
            self.keyboard.text("/targetnext")

        time.sleep(0.7)
        self.keyboard.enter()
        pass

    def select_target(self, target):
        x = target.x + self.capture.offset_x + (target.w / 2)
        y = target.y + self.capture.offset_y + (target.h / 2) + 30
        self.keyboard.mouse_click(self.keyboard.KEY_MOUSE_LEFT, (x, y))
        time.sleep(0.5)

    def move(self, x, y):
        x = x + self.capture.offset_x
        y = y + self.capture.offset_y
        self.keyboard.mouse_click(self.keyboard.KEY_MOUSE_LEFT, (x, y))

    def scroll_screen(self, is_left=False):
        center_x, center_y = self.capture.center

        self.keyboard.mouse_move(center_x, center_y)
        time.sleep(0.2)
        self.keyboard.mouse_down(self.keyboard.KEY_MOUSE_RIGHT)
        if is_left:
            self.keyboard.mouse_move(center_x - 100, center_y)
        else:
            self.keyboard.mouse_move(center_x + 100, center_y)
        time.sleep(0.2)
        self.keyboard.mouse_up(self.keyboard.KEY_MOUSE_RIGHT)


class HandlerSpoilerAutoFarm(BaseHandler):
    logger = logging.getLogger("SpoilerAutoFarm")

    STATE_TARGET = 1
    STATE_FIGHT = 2
    STATE_POST_FIGHT = 3
    STATE_POST_AFTER_FIGHT = 4

    TARGET_NEXT = 1
    TARGET_MOUSE = 2
    TARGET_COMMAND = 3

    target_mouse_counter = 0
    target_state = TARGET_NEXT

    just_killed = False
    got_stuck = False
    action_used = False
    last_killed_target = None

    def __init__(self, controller: ControllerSpoilerAutoFarm, near_target_parser: NearTargetParser,
                 target_parser: TargetParser, mobs=None):

        if mobs is None:
            mobs = []

        self.target_parser = target_parser
        self.near_target_parser = near_target_parser
        self.controller = controller
        self.mobs = mobs

    def _on_tick(self, screen_rgb, screen_gray, delta):
        # We need target all time
        target = self.target_parser.parse(screen_rgb, screen_gray)

        if self.state == STATE_IDLE:
            self.state = self.STATE_TARGET

        if self.state == self.STATE_TARGET:
            return self._handle_state_target(screen_rgb, screen_gray, target)

        if self.state == self.STATE_FIGHT:
            return self._handle_state_fight(screen_rgb, screen_gray, target, delta
                                            )
        if self.state == self.STATE_POST_FIGHT:
            return self._handle_state_post_fight(screen_rgb, screen_gray, target, delta)

        return False

    def _handle_state_target(self, screen_rgb, screen_gray, target):
        if target.exist:
            self.logger.info("State TARGET. Target exist. Agr or target found.")
            self.state = self.STATE_FIGHT
            self.target_mouse_counter = 0
            self.target_state = self.TARGET_NEXT
            self.controller.attack()
            return True

        if self.target_state == self.TARGET_NEXT:
            self.controller.next_target(None)
            self.target_state = self.TARGET_MOUSE
            return True

        if self.target_state == self.TARGET_MOUSE:
            if self.target_mouse_counter >= 2:
                self.target_mouse_counter = 0
                self.controller.move(screen_rgb.shape[1] / 2, screen_rgb.shape[0] / 2)
                self.logger.warning("STATE TARGET. Cannot select target by mouse. Stop and retry")
                return True

            target = self._find_target(screen_rgb, screen_gray)
            if target is not None:
                self.controller.select_target(target)
                self.target_mouse_counter = self.target_mouse_counter + 1
                self.logger.info("State TARGET. Target selected by mouse, distance %s", target.distance)
                return True
            else:
                self.target_state = self.TARGET_COMMAND

        if self.target_state == self.TARGET_COMMAND and self.mobs:
            # TODO need to select agro mobs.s
            aggrs = list(filter(lambda mob: mob["is_aggr"], self.mobs))
            if aggrs:
                mob = random.choice(aggrs)
            else:
                mob = random.choice(self.mobs)

            self.controller.next_target(mob["name"])
            self.logger.info("State IDLE. Target selected by command-> %s", mob["name"])
            return True

        return False

    def _handle_state_fight(self, screen_rgb, screen_gray, target, delta):
        if not target.exist:
            self.logger.warning("State FIGHT, Target not exist. Reset state")
            self._reset(screen_rgb)
            return True

        if target.exist and target.hp == 0:
            self.logger.info("State FIGHT, Target killed")
            self.state = self.STATE_POST_FIGHT
            return True

        if delta > 10 and target.hp >= 99:
            self.logger.info("State FIGHT, Probably got stuck. Reset state")
            self.got_stuck = True
            self._reset(screen_rgb)
            return True

        if not self.action_used and target.hp <= 80:
            self.logger.info("State FIGHT, Use action")
            self.controller.spoil()
            time.sleep(0.2)
            self.controller.manor()
            self.action_used = True

        if int(delta) % 3 == 0:
            self.controller.attack()
        self.logger.info("State FIGHT, Keep fighting. Target hp %s", target.hp)
        return False

    def _handle_state_post_fight(self, screen_rgb, screen_gray, target, delta):
        self.logger.warning("State POST FIGHT, Target not exist. Reset state")

        if target.exist:
            # self.controller.harvest()
            # time.sleep(0.2)
            self.controller.sweep()
            time.sleep(0.3)

        self.controller.pick_up()
        time.sleep(0.3)
        self.controller.pick_up()
        time.sleep(0.3)
        self.controller.pick_up()
        time.sleep(0.3)
        self.controller.pick_up()
        self.controller.cancel()

        self.state = STATE_IDLE
        self.action_used = False
        self.just_killed = True

        return False

    def _reset(self, screen_rgb):
        self.controller.cancel()
        self.controller.move(screen_rgb.shape[1] / 2, screen_rgb.shape[0] / 2)
        self.just_killed = False
        self.last_killed_target = None
        self.state = STATE_IDLE

    def _find_target(self, screen_rgb, screen_gray):
        targets = self.near_target_parser.parse(screen_rgb, screen_gray)


        interested_mobs = []
        for target in targets:
            for mob in self.mobs:
                if fuzz.ratio(target.name.lower(), mob["name"].lower()) >= 70 and target.name != "Taro":
                    interested_mobs.append(target)


        #TODO nearest killed mob still selecting. Use last_killed_target
        if interested_mobs:
            if self.just_killed and len(interested_mobs) > 1 and interested_mobs[0].distance > 70:
                # return second mob if nearest distance below 60. prevent selection of dead monster
                self.just_killed = False
                return interested_mobs[1]
            else:
                return interested_mobs[0]
