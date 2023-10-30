import logging

from src.bot.base import BehaviourHandler
from src.controller import BaseController


class ControllerUseBottles(BaseController):
    def use_bottle(self):
        self.keyboard.f11()


class HandlerUseBottles(BehaviourHandler):
    logger = logging.getLogger("HandlerUseBottles")

    def __init__(self, controller: ControllerUseBottles):
        self.controller = controller

    def _on_tick(self, delta):
        self.controller.use_bottle()
        return 1190
