from abc import ABC, abstractmethod

from app.bot.base import BaseHandler
from app.controller import BaseController


class ControllerSpoilerAutoFarm(BaseController, ABC):
    @abstractmethod
    def spoil(self):
        pass

    @abstractmethod
    def sweep(self):
        pass

    @abstractmethod
    def manor(self):
        pass

    @abstractmethod
    def harvest(self):
        pass

    @abstractmethod
    def pick_up(self):
        pass

    @abstractmethod
    def next_target(self):
        pass

    @abstractmethod
    def select_target(self):
        pass


class HandlerSpoilerAutoFarm(BaseHandler):
    def __init__(self, controller: ControllerSpoilerAutoFarm):
        self.controller = controller

    def _on_tick(self, screen_rgb, screen_grey, time, delta):
        pass

