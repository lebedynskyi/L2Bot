from abc import ABC, abstractmethod
from datetime import datetime

import pyautogui

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.02


def apply_click(button=None):
    if button is None:
        pyautogui.mouseDown()
        pyautogui.mouseUp()
    else:
        pyautogui.mouseDown(int(button[0]), int(button[1]))
        pyautogui.mouseUp(int(button[0]), int(button[1]))


def apply_move(button):
    pyautogui.moveTo(int(button[0]), int(button[1]))


class BaseHandler(ABC):
    last_action_time = 0
    paused = False

    def on_tick(self, screen_rgb, current_time):
        if not self.paused:
            last_action_delta = current_time - self.last_action_time
            self._on_tick(screen_rgb, current_time, last_action_delta)

    @abstractmethod
    def _on_tick(self, screen_rgb, current_time, last_action_delta):
        raise NotImplementedError("Base handlers is not implemented")

    def write_log(self, tag, msg):
        time = datetime.now()
        print("|{0}|  {1}: {2}".format(time, tag, msg))

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False
