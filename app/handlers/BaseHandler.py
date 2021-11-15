from abc import ABC, abstractmethod
from datetime import datetime


class BaseHandler(ABC):
    last_action_time = 0
    is_paused = False

    def __init__(self, keyboard):
        self.keyboard = keyboard

    def on_tick(self, screen_rgb, current_time):
        if not self.is_paused:
            last_action_delta = current_time - self.last_action_time
            self._on_tick(screen_rgb, current_time, last_action_delta)

    @abstractmethod
    def _on_tick(self, screen_rgb, current_time, last_action_delta):
        raise NotImplementedError("Base handlers is not implemented")

    def write_log(self, tag, msg):
        time = datetime.now()
        print("|{0}|  {1}: {2}".format(time, tag, msg))

    def pause(self):
        self.is_paused = True

    def resume(self):
        self.is_paused = False

    # def apply_mouse_click(self, cords=None):
    #     if cords is None:
    #         self.keyboard.mouseDown()
    #         self.keyboard.mouseUp()
    #     else:
    #         self.keyboard.mouseDown(int(cords[0]), int(cords[1]))
    #         self.keyboard.mouseUp(int(cords[0]), int(cords[1]))
    #
    # def apply_mouse_move(self, cords):
    #     self.keyboard.mouse_move(int(cords[0]), int(cords[1]))
