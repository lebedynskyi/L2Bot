import sys

import cv2

from app.handlers.BaseHandler import BaseHandler


class UserDeathHandler(BaseHandler):
    def __init__(self, keyboard, death_parser):
        super().__init__(keyboard)
        self.death_parser = death_parser

    def _on_tick(self, screenshot_image, current_time, last_action_delta):
        if last_action_delta >= 15:
            is_dead = self.death_parser.parse_image(screenshot_image)
            self.last_action_time = current_time
            if is_dead:
                self.write_log("Death", "Player dead")
                cv2.imwrite("res/output/last_death.png", screenshot_image)
                self.kill_game()
            else:
                self.write_log("Death", "Player is alive")

    def kill_game(self):
        import wmi
        f = wmi.WMI()
        for process in f.Win32_Process():
            name = process.name
            print(name)
            if name == "L2.bin":
                process.Terminate()
                self.write_log("Death", "Game killed")
                break
        else:
            self.write_log("Death", "Game not found")

        sys.exit(1)
