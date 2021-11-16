from app.handlers.BaseHandler import BaseHandler


class UseBottlesHandler(BaseHandler):
    def __init__(self, keyboard):
        super().__init__(keyboard)

        self.KEY_ALACRITY = keyboard.KEY_F10

    def _on_tick(self, screen_rgb, current_time, last_action_delta):
        if last_action_delta > 1195:
            self.keyboard.press(self.KEY_ALACRITY)
            self.last_action_time = current_time
            self.write_log("Buff", "use alacrity")


class SelfBuffHandler(BaseHandler):
    def _on_tick(self, screen_rgb, current_time, last_action_delta):
        pass
