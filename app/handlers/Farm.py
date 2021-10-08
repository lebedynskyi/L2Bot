import pyautogui
from app.handlers.BaseHandler import BaseHandler

KEY_NEXT_TARGET = "F1"
KEY_SPOIL = "F2"
KEY_SWEEP = "F3"
KEY_PICK = "F4"
KEY_SEED = "F5"
KEY_HARVEST = "F6"

KEY_FAST_HP = "F8"

STATE_SPOIL = 1
STATE_SEED = 2
STATE_HARVEST = 3
STATE_SWEEP = 4
STATE_PICK = 5


class FarmHandler(BaseHandler):
    current_state = STATE_SPOIL
    has_target = False

    def __init__(self, target_parser, use_manor=True):
        self.target_parser = target_parser
        self.use_manor = use_manor

    def _on_tick(self, screen_rgb, current_time, last_action_delta):
        self.has_target = self.target_parser.parse_image(screen_rgb)
        if self.has_target:
            self.write_log("Farm", "Target exist")
            action_performed = self.handle_has_target(last_action_delta)
        else:
            self.write_log("Farm", "Target not exist")
            action_performed = self.handle_no_target(last_action_delta)

        if action_performed:
            self.last_action_time = current_time

    def handle_no_target(self, last_action_delta):
        if last_action_delta >= 0.5:
            self.current_state = STATE_SPOIL
            pyautogui.press(KEY_NEXT_TARGET)
            return True

        return False

    def handle_has_target(self, last_action_delta):
        if STATE_SPOIL == self.current_state and last_action_delta >= 0.5:
            pyautogui.press(KEY_SPOIL)

            if self.use_manor:
                self.current_state = STATE_SEED
            else:
                self.current_state = STATE_SWEEP
            return True

        if STATE_SEED == self.current_state and last_action_delta >= 0.75:
            pyautogui.press(KEY_SEED)
            self.current_state = STATE_HARVEST
            return True

        if STATE_HARVEST == self.current_state and last_action_delta >= 0.5:
            pyautogui.press(KEY_HARVEST)
            self.current_state = STATE_SWEEP
            return True

        if STATE_SWEEP == self.current_state and last_action_delta >= 0.3:
            pyautogui.press(KEY_SWEEP)
            self.current_state = STATE_PICK
            return True

        if STATE_PICK == self.current_state and last_action_delta >= 0.3:
            pyautogui.press(KEY_PICK, presses=2, interval=0.3)
            self.current_state = STATE_SPOIL
            return True

        return False
