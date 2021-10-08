import pyautogui

from app.handlers.Farm import FarmHandler, STATE_SPOIL

STATE_HIT = -1

KEY_HIT = "F11"


class FarmMobTransformer(FarmHandler):
    has_target = False

    def __init__(self, target_parser, transform_parser, use_manor=True):
        super().__init__(target_parser, use_manor)
        self.transform_parser = transform_parser

    def handle_has_target(self, last_action_delta, screen_rgb):
        if self.current_state == STATE_SPOIL and not self.transform_parser.parse_image(screen_rgb):
            pyautogui.press(KEY_HIT)
        else:
            super().handle_has_target(last_action_delta, screen_rgb)
