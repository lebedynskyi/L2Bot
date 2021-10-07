import time
from abc import ABC, abstractmethod
from datetime import datetime

import pyautogui


class BaseLogic(ABC):
    last_action_time = 0
    paused = False

    def on_tick(self, screen_rgb, current_time):
        last_action_delta = current_time - self.last_action_time
        if not self.paused:
            self._on_tick(screen_rgb, current_time, last_action_delta)

    @abstractmethod
    def _on_tick(self, screen_rgb, current_time, last_action_delta):
        raise NotImplementedError("Base logic is not implemented")

    def write_log(self, tag, msg):
        time = datetime.now()
        print("|{0}|  {1}: {2}".format(time, tag, msg))

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False

    def apply_click(self, button):
        pyautogui.mouseDown(int(button[0]), int(button[1]))
        time.sleep(0.2)
        pyautogui.mouseUp(int(button[0]), int(button[1]))

    def apply_move(self, button):
        pyautogui.moveTo(int(button[0]), int(button[1]), duration=0.2)
