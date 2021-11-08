import random

import pyautogui

from app.handlers.BaseHandler import BaseHandler

KEY_NEXT_TARGET = "1"
KEY_HIT = "2"
KEY_PICK = "4"
KEY_SEED = "F5"
KEY_HARVEST = "F6"
KEY_STUN = "F11"
KEY_ENTER = "ENTER"
KEY_CLEAR_TARGET = "ESC"

STATE_HIT = -1
STATE_TARGET = 0
STATE_SEED = 2
STATE_HARVEST = 3
STATE_PICK = 5

LOG_TAG = "ShamanFarm"


class OrcShamanFarmHandler(BaseHandler):
    current_state = STATE_TARGET
    has_target = False

    def __init__(self, target_window_parser, target_hp_parser, use_manor=True):
        self.use_manor = use_manor
        self.target_hp_parser = target_hp_parser
        self.target_parser = target_window_parser

    def _on_tick(self, screen_rgb, current_time, last_action_delta):
        action_performed = self.handle_state(last_action_delta, screen_rgb)

        if action_performed:
            self.last_action_time = current_time

    def handle_state(self, last_action_delta, screen_rgb):
        target_window = self.target_parser.parse_image(screen_rgb)
        self.has_target = target_window is not None

        if self.current_state == STATE_TARGET and last_action_delta >= 2:
            if self.has_target:
                self.current_state = STATE_SEED if self.use_manor else STATE_HIT
                pyautogui.press(KEY_HIT)
            else:
                self.write_log(LOG_TAG, "Looking for target")
                pyautogui.press(KEY_NEXT_TARGET)
            return True

        if STATE_SEED == self.current_state and last_action_delta >= 2:
            pyautogui.press(KEY_SEED)
            self.current_state = STATE_HIT
            return True

        if STATE_HIT == self.current_state and last_action_delta >= 1:
            target_hp = self.target_hp_parser.parse_image(target_window)
            self.write_log(LOG_TAG, "Target HP {}%".format(target_hp))
            if target_hp is not None and target_hp <= 0:
                self.current_state = STATE_HARVEST if self.use_manor else STATE_PICK
                self.write_log(LOG_TAG, "Mob killed".format(target_hp))
                return True
            elif last_action_delta > random.randint(5, 10):
                self.write_log(LOG_TAG, "Attack mob".format(target_hp))
                pyautogui.press(KEY_HIT)
                return True

            return False

        if STATE_HARVEST == self.current_state and last_action_delta >= 0.75:
            pyautogui.press(KEY_HARVEST)
            self.current_state = STATE_PICK
            return True

        if STATE_PICK == self.current_state and last_action_delta >= 0.75:
            # we need to clear target here in case mob was not spoiled and prevent entering loop with dead mob.
            # Also it will speed up selection of next target
            pyautogui.press(KEY_CLEAR_TARGET)
            pyautogui.press(KEY_PICK, presses=random.randint(2, 3), interval=0.5)
            self.current_state = STATE_TARGET
            return True

        return False
