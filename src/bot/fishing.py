from abc import ABC, abstractmethod

from src.bot.base import BaseHandler

STATE_IDLE = 0
STATE_FISHING = 1
STATE_FIGHTING = 2


class ControllerFishing(ABC):
    @abstractmethod
    def fishing(self):
        pass

    @abstractmethod
    def pumping(self):
        pass

    @abstractmethod
    def reeling(self):
        pass


class HandlerFishing(BaseHandler):
    def __init__(self, controller: ControllerFishing, keyboard, res):
        super().__init__(keyboard, res)
        self.controller = controller
        self.state = STATE_IDLE

    def _on_tick(self, screen_rgb, screen_grey, time, delta):
        pass
