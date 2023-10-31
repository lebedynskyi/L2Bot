import logging
import random
import time

from fuzzywuzzy import fuzz

from src.base import Capture
from src.bot.base import BehaviourHandler
from src.controller import BaseController
from src.keyboard import BaseKeyboard
from src.vision import Vision


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
        self.keyboard.enter()
        time.sleep(0.1)
        if target is not None:
            self.keyboard.text("/target %s" % target)
            time.sleep(0.5)
        else:
            self.keyboard.text("/targetnext")
            time.sleep(0.3)

        self.keyboard.enter()
        pass

    def select_target(self, target):
        x = target.x + self.capture.offset_x + (target.w / 2)
        y = target.y + self.capture.offset_y + (target.h / 2) + 40
        self.keyboard.mouse_click(self.keyboard.KEY_MOUSE_LEFT, (x, y))

    def move(self, point):
        x, y = point
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


class HandlerSpoilerAutoFarm(BehaviourHandler):
    logger = logging.getLogger("SpoilerAutoFarm")

    STATE_TARGET = 1
    STATE_FIGHT = 2
    STATE_POST_FIGHT = 3

    TARGET_NEXT = 1
    TARGET_MOUSE = 2
    TARGET_COMMAND = 3

    target_mouse_counter = 0
    target_state = TARGET_NEXT

    use_spoil = True
    use_manor = False
    use_next_target = False
    just_killed = False
    # TODO use this variable
    got_stuck = False
    action_used = False
    last_killed_target = None
    default_delay = 0.2
    start_fight_time = 0

    def __init__(self, controller: ControllerSpoilerAutoFarm, vision: Vision, mobs=None):
        if mobs is None:
            mobs = []

        self.vision = vision
        self.controller = controller
        self.mobs = mobs
        self.state = self.STATE_TARGET

    def _on_tick(self, delta):
        if self.state == self.STATE_TARGET:
            return self._handle_state_target()
        if self.state == self.STATE_FIGHT:
            return self._handle_state_fight()
        if self.state == self.STATE_POST_FIGHT:
            return self._handle_state_post_fight()

        return False

    def _handle_state_target(self):
        target = self.vision.target()

        if target.exist:
            self.start_fight_time = time.time()
            self.logger.info("State TARGET. Target exist. Agr or target found.")
            self.controller.attack()
            self.state = self.STATE_FIGHT
            self.target_state = self.TARGET_NEXT
            self.target_mouse_counter = 0
            return

        if self.target_state == self.TARGET_NEXT:
            if self.use_next_target:
                self.controller.next_target(None)
            self.target_state = self.TARGET_MOUSE
            return

        if self.target_state == self.TARGET_MOUSE:
            if self.target_mouse_counter >= 2:
                self.logger.warning("STATE TARGET. Cannot select target by mouse. Stop and retry")
                self.target_mouse_counter = 0
                self.controller.move(self.vision.capture.center)
                # ping + delay for drawing
                return 2

            target = self._find_target()
            # no visible target on screen
            if target is not None:
                self.controller.select_target(target)
                self.target_mouse_counter = self.target_mouse_counter + 1
                self.logger.info("State TARGET. Target selected by mouse, distance %s", target.distance)
                # ping + delay for drawing
                return self.default_delay
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

    def _handle_state_fight(self):
        target = self.vision.target()

        if not target.exist:
            self.logger.warning("State FIGHT, Target not exist. Reset state")
            self._reset()
            return

        if target.exist and target.hp == 0:
            self.logger.info("State FIGHT, Target killed")
            self.state = self.STATE_POST_FIGHT
            return 0.5

        if time.time() - self.start_fight_time > 10 and target.hp >= 99:
            self.logger.info("State FIGHT, Probably got stuck. Reset state")
            self.got_stuck = True
            self._reset()
            return self.default_delay

        if int(time.time() - self.start_fight_time) % 3 == 0:
            self.controller.attack()
            return

        if not self.action_used and target.hp <= 80:
            self.logger.info("State FIGHT, Use action if need. Target hp %s", target.hp)

            if self.use_spoil:
                self.controller.spoil()
                self.controller.spoil()
                time.sleep(0.3)

            if self.use_manor:
                self.controller.manor()
                self.controller.manor()
                time.sleep(0.3)

            self.action_used = True
            return

        if target.hp >= 99:
            self.logger.info("State FIGHT, Move to Target. Target hp %s", target.hp)
        else:
            self.logger.info("State FIGHT, Keep fighting. Target hp %s", target.hp)

        return .5

    def _handle_state_post_fight(self):
        self.logger.warning("State POST FIGHT. Harvest  / Sweep / PickUp")

        if self.use_manor:
            self.controller.harvest()
            time.sleep(0.1)
            self.controller.harvest()
            time.sleep(0.3)

        if self.use_spoil:
            self.controller.sweep()
            time.sleep(0.2)
            self.controller.sweep()
            time.sleep(0.3)

        self.controller.pick_up()
        time.sleep(0.4)
        self.controller.pick_up()
        time.sleep(0.4)
        self.controller.pick_up()
        time.sleep(0.4)
        self.controller.cancel()

        self.state = self.STATE_TARGET
        self.action_used = False
        self.just_killed = True
        self.start_fight_time = 0

        return False

    def _reset(self):
        self.controller.cancel()
        self.controller.move(self.vision.capture.center)
        self.just_killed = False
        self.last_killed_target = None
        self.start_fight_time = 0
        self.state = self.STATE_TARGET
        self.target_state = self.TARGET_NEXT

    def _find_target(self, ):
        targets = self.vision.near_targets()

        interested_mobs = []
        for target in targets:
            for mob in self.mobs:
                if fuzz.ratio(target.name.lower(), mob["name"].lower()) >= 70 and target.name != "Taro":
                    interested_mobs.append(target)

        # TODO nearest killed mob still selecting. Use last_killed_target
        # return second mob if nearest distance below 70. prevent selection of dead monster
        # Does not work if one mob. After spoil mob is dead.. WTF? How to handle it?

        if interested_mobs:
            if self.just_killed and len(interested_mobs) > 1 and interested_mobs[0].distance > 70:
                self.just_killed = False
                return interested_mobs[1]
            else:
                return interested_mobs[0]
