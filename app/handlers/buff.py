from app.handlers.BaseHandler import BaseHandler
from app.core.controls import keyboard

import pyautogui

KEY_ALACRITY = keyboard.KEY_F10


class UseBottlesHandler(BaseHandler):
    def _on_tick(self, screen_rgb, current_time, last_action_delta):
        if last_action_delta > 1195:
            pyautogui.press(KEY_ALACRITY)
            self.last_action_time = current_time
            self.write_log("Buff", "use alacrity")


class SelfBuffHandler(BaseHandler):
    def _on_tick(self, screen_rgb, current_time, last_action_delta):
        pass
