from app.core.controls import Keyboard
from app.handlers.BaseHandler import BaseHandler

KEY_NEXT_TARGET = Keyboard.KEY_F1
KEY_SPOIL = Keyboard.KEY_F2
KEY_SWEEP = Keyboard.KEY_F3
KEY_PICK = Keyboard.KEY_F4
KEY_SEED = Keyboard.KEY_F5
KEY_HARVEST = Keyboard.KEY_F6
KEY_SKILL = Keyboard.KEY_F11
KEY_ENTER = Keyboard.KEY_ENTER
KEY_CLEAR_TARGET = Keyboard.KEY_ESC

COMMAND_ATTACK = "/attack"

STATE_HIT = -1
STATE_TARGET = 0
STATE_SPOIL = 1
STATE_SEED = 2
STATE_HARVEST = 3
STATE_SWEEP = 4
STATE_PICK = 5

LOG_TAG = "IFarm"


class SpoilManorFarmHandler(BaseHandler):
    current_state = STATE_TARGET
    has_target = False

    def __init__(self, keyboard, target_window_parser, target_hp_parser, use_skills, use_manor=True, use_spoil=True):
        super().__init__(keyboard)
        self.use_skills = use_skills
        self.use_spoil = use_spoil
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
                self.current_state = STATE_SPOIL if self.use_spoil else STATE_SEED if self.use_manor else STATE_HIT
            else:
                self.write_log(LOG_TAG, "Looking for target")
                self.keyboard.press(KEY_NEXT_TARGET)
            return True

        if STATE_SPOIL == self.current_state and last_action_delta >= 0.5:
            self.keyboard.press(KEY_SPOIL)
            self.current_state = STATE_SEED if self.use_manor else STATE_HIT
            return True

        if STATE_SEED == self.current_state and last_action_delta >= 2:
            self.keyboard.press(KEY_SEED)
            self.current_state = STATE_HIT
            return True

        if STATE_HIT == self.current_state and last_action_delta >= 1:
            target_hp = self.target_hp_parser.parse_image(target_window)
            self.write_log(LOG_TAG, "Farming. Target HP {}%".format(target_hp))
            if target_hp is not None and target_hp <= 0:
                self.current_state = STATE_HARVEST if self.use_manor else STATE_SWEEP if self.use_spoil else STATE_PICK
                return True
            elif self.use_skills and target_hp is not None and target_hp <= 6:
                self.keyboard.press(KEY_SKILL)
                return True
            elif last_action_delta > 10:
                self.keyboard.text(COMMAND_ATTACK)
                self.keyboard.press(KEY_ENTER)
                return True

            return False

        if STATE_HARVEST == self.current_state and last_action_delta >= 0.75:
            self.keyboard.press(KEY_HARVEST)
            self.current_state = STATE_SWEEP if self.use_spoil else STATE_PICK
            return True

        if STATE_SWEEP == self.current_state and last_action_delta >= 0.75:
            self.keyboard.press(KEY_SWEEP)
            self.current_state = STATE_PICK
            return True

        if STATE_PICK == self.current_state and last_action_delta >= 0.75:
            # we need to clear target here in case mob was not spoiled and prevent entering loop with dead mob.
            # Also it will speed up selection of next target
            self.keyboard.press(KEY_CLEAR_TARGET)
            self.keyboard.press(KEY_PICK, presses=2, interval=0.75)
            self.current_state = STATE_TARGET
            return True

        return False
