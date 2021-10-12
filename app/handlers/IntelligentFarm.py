import pyautogui

from app.handlers.BaseHandler import BaseHandler

KEY_NEXT_TARGET = "F1"
KEY_SPOIL = "F2"
KEY_SWEEP = "F3"
KEY_PICK = "F4"
KEY_SEED = "F5"
KEY_HARVEST = "F6"
KEY_STUN = "F11"
KEY_CLEAR_TARGET = "ESC"

STATE_HIT = -1
STATE_TARGET = 0
STATE_SPOIL = 1
STATE_SEED = 2
STATE_HARVEST = 3
STATE_SWEEP = 4
STATE_PICK = 5

LOG_TAG = "IFarm"


class IntelligentFarmHandler(BaseHandler):
    current_state = STATE_TARGET
    has_target = False

    def __init__(self, target_window_parser, target_hp_parser, use_manor=True):
        self.use_manor = use_manor
        self.target_hp_parser = target_hp_parser
        self.target_parser = target_window_parser

    def _on_tick(self, image_rgb, current_time, last_action_delta):
        action_performed = self.handle_state(last_action_delta, image_rgb)

        if action_performed:
            self.last_action_time = current_time

    def handle_state(self, last_action_delta, screen_rgb):
        target_window = self.target_parser.parse_image(screen_rgb)
        self.has_target = target_window is not None

        if self.current_state == STATE_TARGET and last_action_delta >= 1:
            if self.has_target:
                self.current_state = STATE_SPOIL
            else:
                pyautogui.press(KEY_NEXT_TARGET)
            return True

        if STATE_SPOIL == self.current_state and last_action_delta >= 0.5:
            pyautogui.press(KEY_SPOIL)

            if self.use_manor:
                self.current_state = STATE_SEED
            else:
                self.current_state = STATE_HIT
            return True

        if STATE_SEED == self.current_state and last_action_delta >= 2:
            pyautogui.press(KEY_SEED)
            self.current_state = STATE_HIT
            return True

        if STATE_HIT == self.current_state and last_action_delta >= 1:
            target_hp = self.target_hp_parser.parse_image(target_window)
            self.write_log(LOG_TAG, "Farming. Target HP {}%".format(target_hp))
            if target_hp <= 5:
                pyautogui.press(KEY_STUN)
            elif target_hp <= 0:
                if self.use_manor:
                    self.current_state = STATE_HARVEST
                else:
                    self.current_state = STATE_SWEEP
            return True

        if STATE_HARVEST == self.current_state and last_action_delta >= 0.75:
            pyautogui.press(KEY_HARVEST)
            self.current_state = STATE_SWEEP
            return True

        if STATE_SWEEP == self.current_state and last_action_delta >= 0.75:
            pyautogui.press(KEY_SWEEP)
            self.current_state = STATE_PICK
            return True

        if STATE_PICK == self.current_state and last_action_delta >= 0.75:
            # we need to clear target here in case mob was not spoiled and prevent entering loop with dead mob.
            # Also it will speed up selection next target
            pyautogui.press(KEY_CLEAR_TARGET)
            pyautogui.press(KEY_PICK, presses=2, interval=0.75)
            self.current_state = STATE_TARGET
            return True

        return False

    def handle_no_target(self, last_action_delta):
        if last_action_delta >= 0.5:
            self.current_state = STATE_SPOIL
            pyautogui.press(KEY_NEXT_TARGET)
            return True

        return False
