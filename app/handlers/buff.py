from app.handlers.BaseHandler import BaseHandler

STATE_IDLE = 0
STATE_BUFF = 1


class UseBottlesHandler(BaseHandler):
    def __init__(self, keyboard):
        super().__init__(keyboard)

        self.KEY_ALACRITY = keyboard.KEY_F10

    def _on_tick(self, screen_rgb, current_time, last_action_delta):
        if last_action_delta > 1050:
            self.keyboard.press(self.KEY_ALACRITY)
            self.last_action_time = current_time
            self.write_log("Buff", "use alacrity")


class SelfBuffHandler(BaseHandler):
    current_state = STATE_IDLE

    def __init__(self, keyboard, farm_logic):
        super().__init__(keyboard)
        self.farm_logic = farm_logic
        self.KEY_BUF_MACRO = keyboard.KEY_F10
        self.KEY_CLEAR_TARGET = keyboard.KEY_ESC

    def _on_tick(self, screen_rgb, current_time, last_action_delta):
        action_performed = self.handle_state(last_action_delta)
        if action_performed:
            self.last_action_time = current_time

    def handle_state(self, last_action_delta):
        if self.current_state == STATE_IDLE and last_action_delta > 19 * 60 and not self.farm_logic.has_target:
            self.write_log("BUFF", "Rebuff in progress")
            self.farm_logic.pause()
            self.keyboard.press(self.KEY_BUF_MACRO)
            self.current_state = STATE_BUFF
            return True

        if self.current_state == STATE_BUFF and last_action_delta > 40:
            self.write_log("BUFF", "Clear target continue farm")
            self.keyboard.press(self.KEY_CLEAR_TARGET)
            self.farm_logic.resume()
            self.current_state = STATE_IDLE
            return True

        return False
