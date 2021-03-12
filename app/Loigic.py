from datetime import datetime

import numpy as np
import pyautogui
from PIL import ImageGrab


class Logic:
    def __init__(self, dialog_parser, captcha_parser, captcha_solver):
        self.dialog_parser = dialog_parser
        self.captcha_parser = captcha_parser
        self.captcha_solver = captcha_solver

    def check_captcha(self):
        screenshot = ImageGrab.grab()
        screenshot_image = np.array(screenshot)
        dialog, ok_position, cancel_position = self.dialog_parser.parse_image(screenshot_image)
        if dialog is None:
            print("%s Loop: no warning found" % datetime.now())
            return

        captcha_text = self.captcha_parser.parse_image(dialog)
        if self.captcha_solver.is_ariphmetic:
            result = self.captcha_solver.solve_math(captcha_text)
        else:
            result = self.captcha_solver.solve_logic(captcha_text)

        if result:
            return ok_position
        else:
            return cancel_position

    def apply_move(self, button):
        pyautogui.moveTo(button[0], button[1])

    def apply_click(self, button):
        pyautogui.leftClick(button[0], button[1])
