import time

import pyautogui

from app.logic.BaseLogic import BaseLogic

KEY_GREATER_HEAL = "F12"
KEY_TARGET_PET = "F7"
KEY_KILL_PET = "F8"
KEY_RES_PET = "F9"
KEY_CLEAR_TARGET = "ESC"


class PetManaLogic(BaseLogic):
    def __init__(self, hp_parser, target_logic):
        self.hp_parser = hp_parser
        self.target_logic = target_logic

    def on_tick(self, screen_rgb, current_time):
        last_action_delta = current_time - self.last_action_time
        if last_action_delta >= 10 and not self.target_logic.has_target:
            self.last_action_time = current_time
            hp = self.hp_parser.parse_image(screen_rgb)
            if hp is not None and int(hp[0]) < 2500:
                self.kill_res_pet()

    def kill_res_pet(self):
        # pyautogui.press(KEY_GREATER_HEAL)
        # time.sleep(1)

        pyautogui.press(KEY_TARGET_PET)
        time.sleep(1)
        pyautogui.press(KEY_KILL_PET)
        time.sleep(10)
        pyautogui.press(KEY_RES_PET)
        time.sleep(30)

        pyautogui.press(KEY_CLEAR_TARGET, presses=2, interval=0.5)
