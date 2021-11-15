import time

import random

import cv2

from app.core.controls import Keyboard
from app.handlers.BaseHandler import BaseHandler

greetings = ["kek", "hi", "plololo", "omg", "Hello"]

question = ["Why??", "And why ?", "lol"]

msg = ["Why you TP me?. I just farmed", "For whrat? Did'nt do anything.. just farming", "omg. i just was farming"]

KEY_SIT = Keyboard.KEY_F12
KEY_ENTER = "ENTER"

TELEPORT_TAG = "Teleport"


class UserTeleportedHandler(BaseHandler):
    was_teleported = False

    def __init__(self, color_parser, handlers_to_pause):
        self.handlers_to_pause = handlers_to_pause
        self.color_parser = color_parser

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
        self.keyboard.press(KEY_ENTER)

        time.sleep(3)
        self.keyboard.text(random.choice(question))
        self.keyboard.press(KEY_ENTER)

        time.sleep(4)
        self.keyboard.text(random.choice(msg))
        self.keyboard.press(KEY_ENTER)

        time.sleep(5)
        self.keyboard.press(KEY_SIT)

        cv2.imwrite("res/output/after_teleport.png", screen)
