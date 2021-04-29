import time
from datetime import datetime
import cv2
import numpy as np
import pyautogui

from PIL import ImageGrab


class CaptchaLogic:
    def __init__(self, dialog_parser, captcha_parser, group_parser, captcha_solver, player):
        self.dialog_parser = dialog_parser
        self.captcha_parser = captcha_parser
        self.captcha_solver = captcha_solver
        self.group_parser = group_parser
        self.player = player

    def check_captcha(self):
        screenshot = ImageGrab.grab()
        screenshot_image = np.array(screenshot)
        solo_answer = self._check_antibot_captcha(screenshot_image)
        if not solo_answer:
            return self._check_group_captcha(screenshot_image)
        else:
            return solo_answer

    def _check_antibot_captcha(self, screenshot_image):
        dialog, ok_position, cancel_position = self.dialog_parser.parse_image(screenshot_image)
        if dialog is None:
            print("%s Loop: no warning found" % datetime.now())
            return

        self.player.play_captcha()

        for scale in range(500, 800, 100):
            try:
                captcha_text = self.captcha_parser.parse_image(dialog, scale)
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
                print("Cannot solve captcha, it was scale  %s " % scale)
                print(e)
                cv2.imwrite("output/last_error.png", screenshot_image)
        self.player.play_warning()

    def _check_group_captcha(self, screenshot_image):
        result = self.group_parser.parse_image(screenshot_image)
        if not result:
            print("%s Loop: no group found" % datetime.now())

        return result

    def apply_move(self, button):
        pyautogui.moveTo(int(button[0]), int(button[1]), duration=0.2)

    def apply_click(self, button):
        pyautogui.mouseDown(int(button[0]), int(button[1]))
        time.sleep(0.2)
        pyautogui.mouseUp(int(button[0]), int(button[1]))
