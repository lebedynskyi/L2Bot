import sys

import cv2

from app.logic.BaseLogic import BaseLogic


class UserDeathLogic(BaseLogic):
    def __init__(self, death_parser):
        self.death_parser = death_parser

    def _on_tick(self, screenshot_image, current_time):
        is_dead = self.death_parser.parse_image(screenshot_image)
        if is_dead:
            self.write_log("Death", "User dead")
            cv2.imwrite("output/last_death.png", screenshot_image)
            self.kill_game()

    def kill_game(self):
        import wmi
        f = wmi.WMI()
        for process in f.Win32_Process():
            name = process.name
            print(name)
            if name == "l2.exe":
                process.Terminate()
                self.write_log("Death", "Game killed")
        else:
            self.write_log("Death", "Game not found")

        sys.exit(1)
