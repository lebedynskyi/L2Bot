from abc import ABC, abstractmethod
from datetime import datetime


class BaseLogic(ABC):
    last_action_time = 0

    @abstractmethod
    def on_tick(self, screen_rgb, current_time):
        raise NotImplementedError("Base logic is not implemented")

    def write_log(self, tag, msg):
        time = datetime.now()
        print("|{0}|  {1}: {2}".format(time, tag, msg))
