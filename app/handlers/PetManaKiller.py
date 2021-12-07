from app.handlers.BaseHandler import BaseHandler

STATE_IDLE = 0
STATE_TARGET_PET = 1
STATE_KILL_PET = 2
STATE_RES_PET = 3
STATE_RESUME_FARM = 4
KILL_PET_LIMIT = 2000


class PetManaHandler(BaseHandler):
    current_state = STATE_IDLE

    def __init__(self, keyboard, hp_parser, farm_logic):
        super().__init__(keyboard)
        self.KEY_TARGET_PET = keyboard.KEY_F7
        self.KEY_KILL_PET = keyboard.KEY_F8
        self.KEY_RES_PET = keyboard.KEY_F9
        self.KEY_CLEAR_TARGET = keyboard.KEY_ESC
        self.hp_parser = hp_parser
        self.farm_logic = farm_logic

    def _on_tick(self, screen_rgb, current_time, last_action_delta):
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
            self.keyboard.press(self.KEY_TARGET_PET)
            self.current_state = STATE_KILL_PET
            self.write_log("HPLogic", "Pet in target")
            return True

        if self.current_state == STATE_KILL_PET and last_action_delta >= 1:
            self.keyboard.press(self.KEY_KILL_PET)
            self.current_state = STATE_RES_PET
            self.write_log("HPLogic", "Killing pet")
            return True

        if self.current_state == STATE_RES_PET and last_action_delta >= 10:
            self.keyboard.press(self.KEY_RES_PET)
            self.current_state = STATE_RESUME_FARM
            self.write_log("HPLogic", "Res the pet")
            return True

        if self.current_state == STATE_RESUME_FARM and last_action_delta >= 25:
            self.keyboard.press(self.KEY_CLEAR_TARGET, presses=2, interval=0.5)
            self.current_state = STATE_IDLE
            self.farm_logic.resume()
            self.write_log("HPLogic", "Pet is alive. Continue farm")
            return True

        return False


class PetManaTimerHandler(BaseHandler):
    current_state = STATE_IDLE

    def __init__(self, keyboard, farm_logic):
        super().__init__(keyboard)
        self.KEY_TARGET_PET = keyboard.KEY_F7
        self.KEY_KILL_PET = keyboard.KEY_F8
        self.KEY_RES_PET = keyboard.KEY_F9
        self.KEY_CLEAR_TARGET = keyboard.KEY_ESC
        self.farm_logic = farm_logic

    def _on_tick(self, screen_rgb, current_time, last_action_delta):
        action_performed = self.handle_state(last_action_delta, screen_rgb)

        if action_performed:
            self.last_action_time = current_time

    def handle_state(self, last_action_delta, screen_rgb):
        if self.current_state == STATE_IDLE and last_action_delta >= 10 * 60 and not self.farm_logic.has_target:
            self.farm_logic.pause()
            self.current_state = STATE_TARGET_PET
            self.write_log("PetKiller", "Tim to kill Kill the pet")

        if self.current_state == STATE_TARGET_PET and last_action_delta >= 1:
            self.keyboard.press(self.KEY_TARGET_PET)
            self.current_state = STATE_KILL_PET
            self.write_log("PetKiller", "Pet in target")
            return True

        if self.current_state == STATE_KILL_PET and last_action_delta >= 1:
            self.keyboard.press(self.KEY_KILL_PET)
            self.current_state = STATE_RES_PET
            self.write_log("PetKiller", "Killing pet")
            return True

        if self.current_state == STATE_RES_PET and last_action_delta >= 10:
            self.keyboard.press(self.KEY_RES_PET)
            self.current_state = STATE_RESUME_FARM
            self.write_log("PetKiller", "Res the pet")
            return True

        if self.current_state == STATE_RESUME_FARM and last_action_delta >= 15:
            self.keyboard.press(self.KEY_CLEAR_TARGET)
            self.current_state = STATE_IDLE
            self.farm_logic.resume()
            self.write_log("PetKiller", "Pet is alive. Continue farm")
            return True

        return False
