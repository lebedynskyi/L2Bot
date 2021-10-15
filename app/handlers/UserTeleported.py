import time

import random

import cv2
import pyautogui

from app.handlers.BaseHandler import BaseHandler

greetings = ["kek", "hi", "lololo", "omg"]

question = ["Why??", "And why ?"]

msg = ["Why i here?. I just farmed", "For whrat? Did'nt do anything.. Just farming", "omg. i just was farming antelops"]

KEY_SIT = "F12"


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
            if c[0] >= 15 or c[1] >= 15 or c[2] >= 15:
                if self.was_teleported:
                    self.on_teleport_ended(screen_rgb)
                break
        else:
            self.on_teleport_detected()

    def on_teleport_detected(self):
        self.write_log("Teleport", "Detected teleporting. Write some word to chat !")
        self.was_teleported = True

        for h in self.handlers_to_pause:
            h.pause()
            self.write_log("Teleport", "Pause handler {}".format(h))

    def on_teleport_ended(self, screen):
        self.write_log("Teleport", "Teleport finished")
        self.pause()

        time.sleep(1)
        pyautogui.typewrite(random.choice(greetings))
        pyautogui.press("ENTER")

        time.sleep(3)
        pyautogui.typewrite(random.choice(question))
        pyautogui.press("ENTER")

        time.sleep(4)
        pyautogui.typewrite(random.choice(msg))
        pyautogui.press("ENTER")

        time.sleep(5)
        pyautogui.press(KEY_SIT)

        cv2.imwrite("res/output/after_teleport.png", screen)
