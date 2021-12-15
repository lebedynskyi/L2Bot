import random
import time
from app.handlers.base import BaseHandler

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
    target_hp = -1

    def __init__(self, keyboard, target_window_parser, target_hp_parser, use_skills, use_manor=True, use_spoil=True):
        super().__init__(keyboard)
        self.use_skills = use_skills
        self.use_spoil = use_spoil
        self.use_manor = use_manor
        self.target_hp_parser = target_hp_parser
        self.target_parser = target_window_parser

        self.KEY_NEXT_TARGET = keyboard.KEY_F1
        self.KEY_SPOIL = keyboard.KEY_F2
        self.KEY_SWEEP = keyboard.KEY_F3
        self.KEY_PICK = keyboard.KEY_F4
        self.KEY_SEED = keyboard.KEY_F5
        self.KEY_HARVEST = keyboard.KEY_F6
        self.KEY_SKILL = keyboard.KEY_F11
        self.KEY_ENTER = keyboard.KEY_ENTER
        self.KEY_HIT = keyboard.KEY_F12
        self.KEY_CLEAR_TARGET = keyboard.KEY_ESC

    def _on_tick(self, image_rgb, current_time, last_action_delta):
        action_performed = self.handle_state(last_action_delta, image_rgb)

        if action_performed:
            self.last_action_time = current_time

    def handle_state(self, last_action_delta, screen_rgb):
        target_window = self.target_parser.parse_image(screen_rgb)
        self.has_target = target_window is not None
        self.target_hp = self.target_hp_parser.parse_image(target_window)

        if self.current_state == STATE_TARGET and last_action_delta >= round(random.uniform(0.5, 2), 2):
            if self.has_target:
                self.current_state = STATE_SPOIL if self.use_spoil else STATE_SEED if self.use_manor else STATE_HIT
            else:
                self.write_log(LOG_TAG, "Looking for target")
                self.keyboard.press(self.KEY_NEXT_TARGET)
            return True

        if STATE_SPOIL == self.current_state and last_action_delta >= 0.5:
            if self.target_hp < 0:
                self.current_state = STATE_TARGET
                self.keyboard.press(self.KEY_CLEAR_TARGET)
                return True

            self.keyboard.press(self.KEY_SPOIL)
            self.current_state = STATE_SEED if self.use_manor else STATE_HIT
            return True

        if STATE_SEED == self.current_state and last_action_delta >= (2 if self.use_spoil else 0.5):
            if self.target_hp < 0:
                self.current_state = STATE_TARGET
                self.keyboard.press(self.KEY_CLEAR_TARGET)
                return True

            self.keyboard.press(self.KEY_SEED)
            self.current_state = STATE_HIT
            return True

        if STATE_HIT == self.current_state and last_action_delta >= 1:
            if not self.has_target:
                self.write_log(LOG_TAG, "No target reset state")
                self.current_state = STATE_TARGET
                return True

            self.write_log(LOG_TAG, "Farming. Target HP {}%".format(self.target_hp))
            if self.target_hp is not None and self.target_hp <= 0:
                self.current_state = STATE_HARVEST if self.use_manor else STATE_SWEEP if self.use_spoil else STATE_PICK
                return True
            elif self.use_skills and self.target_hp is not None and self.target_hp <= 10:
                self.keyboard.press(self.KEY_SKILL)
                return True
            elif last_action_delta > random.randint(8, 12):
                self.keyboard.press(self.KEY_HIT)
                return True

            return False

        if STATE_HARVEST == self.current_state and last_action_delta >= 0.75:
            self.keyboard.press(self.KEY_HARVEST)
            self.current_state = STATE_SWEEP if self.use_spoil else STATE_PICK
            return True

        if STATE_SWEEP == self.current_state and last_action_delta >= 0.75:
            self.keyboard.press(self.KEY_SWEEP)
            self.current_state = STATE_PICK
            return True

        if STATE_PICK == self.current_state and last_action_delta >= 1:
            # we need to clear target here in case mob was not spoiled and prevent entering loop with dead mob.
            # Also it will speed up selection of next target
            self.keyboard.press(self.KEY_CLEAR_TARGET)
            self.keyboard.press(self.KEY_PICK)
            time.sleep(1)
            self.keyboard.press(self.KEY_PICK)
            self.keyboard.press(self.KEY_NEXT_TARGET)
            self.current_state = STATE_TARGET
            return True

        return False
