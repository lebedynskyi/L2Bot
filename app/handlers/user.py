import os
import random
import sys
import time

import cv2

from app.handlers.base import BaseHandler

TELEPORT_TAG = "Teleport"
DEATH_TAG = "Death"
STATUS_TAG = "Status"

greetings = ["kek", "hi", "plololo", "omg", "Hello"]
question = ["Why??", "And why ?", "lol"]
msg = ["Why you TP me?. I just farmed", "For whrat? Did'nt do anything.. just farming", "omg. i just was farming"]


class UserDeathHandler(BaseHandler):
    def __init__(self, keyboard, death_parser):
        super().__init__(keyboard)
        self.death_parser = death_parser

    def _on_tick(self, screenshot_image, current_time, last_action_delta):
        if last_action_delta >= 15:
            is_dead = self.death_parser.parse_image(screenshot_image)
            self.last_action_time = current_time
            if is_dead:
                self.write_log(DEATH_TAG, "Player dead")
                cv2.imwrite("res/output/last_death.png", screenshot_image)
                self.kill_game()
            else:
                self.write_log(DEATH_TAG, "Player is alive")

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

        # os.system("shutdown /s /t 1")
        sys.exit(1)


class UserStatusHandler(BaseHandler):
    def __init__(self, status_parser, keyboard):
        super().__init__(keyboard)
        self.status_parser = status_parser

    def _on_tick(self, screen_rgb, current_time, last_action_delta):
        if last_action_delta > 10:
            hp = self.status_parser.parse_image(screen_rgb)
            if hp:
                self.write_log(STATUS_TAG, "player HP -> {}/{}".format(hp[0], hp[1]))


class UserTeleportedHandler(BaseHandler):
    was_teleported = False

    def __init__(self, keyboard, color_parser, handlers_to_pause):
        super().__init__(keyboard)
        self.handlers_to_pause = handlers_to_pause
        self.color_parser = color_parser
        self.KEY_SIT = keyboard.KEY_F12
        self.KEY_ENTER = keyboard.KEY_ENTER

    def _on_tick(self, screen_rgb, current_time, last_action_delta):
        x, y = screen_rgb.shape[0], screen_rgb.shape[1]
        center = int(y / 2), int(x / 2)
        point1 = int(center[0] + center[0] / 2), int(center[1] + center[1] / 2)
        point2 = int(center[0] + center[0] / 2), int(center[1] - center[1] / 2)

        colors = self.color_parser.parse_image(screen_rgb, points=[point1, point2])

        for c in colors:
            # Check 3 main colors. When user is teleporting he has a black screen
            if c[0] >= 15 or c[1] >= 15 or c[2] >= 15:
                if self.was_teleported:
                    self.on_teleport_ended(screen_rgb)
                break
        else:
            self.on_teleport_detected()

    def on_teleport_detected(self):
        self.write_log(TELEPORT_TAG, "Detected teleporting. Write some word to chat !")
        self.was_teleported = True

        for h in self.handlers_to_pause:
            h.pause()
            self.write_log(TELEPORT_TAG, "Paused handler {}".format(h))

    def on_teleport_ended(self, screen):
        self.write_log(TELEPORT_TAG, "Teleport finished")
        self.pause()

        time.sleep(1)
        self.keyboard.text(random.choice(greetings))
        self.keyboard.press(self.KEY_ENTER)

        time.sleep(3)
        self.keyboard.text(random.choice(question))
        self.keyboard.press(self.KEY_ENTER)

        time.sleep(4)
        self.keyboard.text(random.choice(msg))
        self.keyboard.press(self.KEY_ENTER)

        time.sleep(5)
        self.keyboard.press(self.KEY_SIT)

        cv2.imwrite("res/output/after_teleport.png", screen)
