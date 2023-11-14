import logging
import time

from src.bot.base import BehaviourHandler
from src.controller import BaseController
from src.vision import Vision


class ControllerRest(BaseController):
    def sit(self):
        self.keyboard.enter()
        time.sleep(0.1)
        self.keyboard.text("/sit")

    def stand(self):
        self.keyboard.enter()
        time.sleep(0.1)
        self.keyboard.text("/stand")


class ControllerUseBottles(BaseController):
    def use_bottle(self):
        self.keyboard.f11()


class HandlerUseBottles(BehaviourHandler):
    logger = logging.getLogger("HandlerUseBottles")

    def __init__(self, controller: ControllerUseBottles):
        self.controller = controller

    def _on_tick(self, delta):
        self.controller.use_bottle()
        return 1190  # almost 20 minutes


class HandlerRest(BehaviourHandler):
    logger = logging.getLogger("HandlerUseBottles")

    def __init__(self, vision: Vision, controller: ControllerUseBottles, *pausable_handler):
        self.vision = vision
        self.controller = controller
        self.pause_handlers = pausable_handler

    def _on_tick(self, delta):
        target = self.vision.target()
        if target.exist:
            return

        user_status = self.vision.user_status()
        if user_status.hp[0] / user_status.hp[1] < 0.3:
            # TODO add states
            # wait till regen
            # continue farm
            pass

    def _pause_handlers(self):
        for p in self.pause_handlers:
            p.is_paused = True

    def _resume_handlers(self):
        for p in self.pause_handlers:
            p.is_paused = False
