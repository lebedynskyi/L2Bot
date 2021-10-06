import pyautogui

from app.logic.BaseLogic import BaseLogic

KEY_GREATER_HEAL = "F12"
KEY_TARGET_PET = "F7"
KEY_KILL_PET = "F8"
KEY_RES_PET = "F9"
KEY_CLEAR_TARGET = "ESC"

STATE_IDLE = 0
STATE_TARGET_PET = 1
STATE_KILL_PET = 2
STATE_RES_PET = 3
STATE_RESUME_FARM = 4

KILL_PET_LIMIT = 2500


class PetManaLogic(BaseLogic):
    current_state = STATE_IDLE

    def __init__(self, hp_parser, farm_logic):
        self.hp_parser = hp_parser
        self.farm_logic = farm_logic

    def _on_tick(self, screen_rgb, current_time):
        last_action_delta = current_time - self.last_action_time

        action_performed = self.handle_state(last_action_delta, screen_rgb)

        if action_performed:
            self.last_action_time = current_time

    def handle_state(self, last_action_delta, screen_rgb):
        if self.current_state == STATE_IDLE and last_action_delta >= 10 and not self.farm_logic.has_target:
            hp = self.hp_parser.parse_image(screen_rgb)
            if hp is not None and int(hp[0]) <= KILL_PET_LIMIT:
                self.farm_logic.pause()
                self.current_state = STATE_TARGET_PET
                self.write_log("HPLogic", "To low hp. Kill the pet")
            return True

        if self.current_state == STATE_TARGET_PET and last_action_delta >= 1:
            pyautogui.press(KEY_TARGET_PET)
            self.current_state = STATE_KILL_PET
            self.write_log("HPLogic", "Pet in target")
            return True

        if self.current_state == STATE_KILL_PET and last_action_delta >= 1:
            pyautogui.press(KEY_KILL_PET)
            self.current_state = STATE_RES_PET
            self.write_log("HPLogic", "Killing pet")
            return True

        if self.current_state == STATE_RES_PET and last_action_delta >= 10:
            pyautogui.press(KEY_RES_PET)
            self.current_state = STATE_RESUME_FARM
            self.write_log("HPLogic", "Res the pet")
            return True

        if self.current_state == STATE_RESUME_FARM and last_action_delta <= 30:
            pyautogui.press(KEY_CLEAR_TARGET, presses=2, interval=0.5)
            self.current_state = STATE_IDLE
            self.farm_logic.resume()
            self.write_log("HPLogic", "Pet is alive. Continue farm")
            return True

        return False
