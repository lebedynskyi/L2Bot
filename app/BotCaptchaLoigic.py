import time
from datetime import datetime
import cv2
import numpy as np
import pyautogui

from PIL import ImageGrab

class Logic:
    def __init__(self, dialog_parser, captcha_parser, captcha_solver, player):
        self.dialog_parser = dialog_parser
        self.captcha_parser = captcha_parser
        self.captcha_solver = captcha_solver
        self.player = player

    def check_captcha(self):
        screenshot = ImageGrab.grab()
        screenshot_image = np.array(screenshot)
        dialog, ok_position, cancel_position = self.dialog_parser.parse_image(screenshot_image)
        if dialog is None:
            print("%s Loop: no warning found" % datetime.now())
            return

        self.player.play_captcha()

        try:
            captcha_text = self.captcha_parser.parse_image(dialog)
            if self.captcha_solver.is_ariphmetic(captcha_text):
                result = self.captcha_solver.solve_math(captcha_text)
            else:
                result = self.captcha_solver.solve_logic(captcha_text)
            cv2.imwrite("output/last_solved_captcha.png", screenshot_image)
            if result:
                return ok_position
            else:
                return cancel_position
        except BaseException as e:
            self.player.play_warning()
            print("Cannot solve captcha")
            print(e)
            print("%s Loop: no warning found" % datetime.now())
            cv2.imwrite("output/last_error.png", screenshot_image)

    def apply_move(self, button):
        pyautogui.moveTo(int(button[0]), int(button[1]), duration=0.2)

    def apply_click(self, button):
        pyautogui.mouseDown(int(button[0]), int(button[1]))
        time.sleep(0.2)
        pyautogui.mouseUp(int(button[0]), int(button[1]))
