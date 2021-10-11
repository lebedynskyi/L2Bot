import pyautogui

from app.handlers.BaseHandler import BaseHandler

KEY_NEXT_TARGET = "F1"
KEY_SPOIL = "F2"
KEY_SWEEP = "F3"
KEY_PICK = "F4"
KEY_SEED = "F5"
KEY_HARVEST = "F6"
KEY_HIT = "F11"

STATE_HIT = -1
STATE_SPOIL = 1
STATE_SEED = 2
STATE_HARVEST = 3
STATE_SWEEP = 4
STATE_PICK = 5

LOG_TAG = "IFarm"


class IntelligentFarmHandler(BaseHandler):
    current_state = STATE_SPOIL
    has_target = False

    def __init__(self, target_window_parser, target_hp_parser):
        self.target_hp_parser = target_hp_parser
        self.target_parser = target_window_parser

    def _on_tick(self, image_rgb, current_time, last_action_delta):
        target_window = self.target_parser.parse_image(image_rgb)
        self.has_target = target_window is not None
        if self.has_target:
            self.write_log("LOG_TAG", "Target exist")
            action_performed = self.handle_has_target(last_action_delta, target_window, image_rgb)
        else:
            self.write_log("LOG_TAG", "Target not exist")
            action_performed = self.handle_no_target(last_action_delta)

        if action_performed:
            self.last_action_time = current_time

    def handle_has_target(last_action_delta, target_window, screen_rgb):
        return False

    def handle_no_target(self, last_action_delta):
        if last_action_delta >= 0.5:
            self.current_state = STATE_SPOIL
            pyautogui.press(KEY_NEXT_TARGET)
            return True

        return False
