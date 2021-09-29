from abc import ABC, abstractmethod
import time


class BaseLogic(ABC):
    last_action_time = 0

    @abstractmethod
    def on_tick(self, screen_rgb, current_time):
        raise NotImplementedError("Base logic is not implemented")
