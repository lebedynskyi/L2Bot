import time
import cv2
import pyautogui

from app.logic.BaseLogic import BaseLogic


class CaptchaLogic(BaseLogic):
    def __init__(self, dialog_parser, captcha_parser, group_parser, captcha_solver):
        self.dialog_parser = dialog_parser
        self.captcha_parser = captcha_parser
        self.captcha_solver = captcha_solver
        self.group_parser = group_parser

    def on_tick(self, screenshot_image, current_time):
        last_action_delta = current_time - self.last_action_time
        answer = None
        if last_action_delta >= 3:
            answer = self._check_anti_bot_captcha(screenshot_image)
            if answer:
                self.apply_click(answer)

        if last_action_delta >= 1:
            answer = self._check_group_captcha(screenshot_image)
            if answer:
                self.apply_click(answer)

        self.last_action_time = current_time
        return answer

    def _check_anti_bot_captcha(self, screenshot_image):
        dialog, ok_position, cancel_position = self.dialog_parser.parse_image(screenshot_image)
        if dialog is None:
            self.write_log("Captcha", "No Solo captcha")
            return

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

    def _check_group_captcha(self, screenshot_image):
        result = self.group_parser.parse_image(screenshot_image)
        if not result:
            self.write_log("Captcha", "No Group captcha")

        return result

    def apply_move(self, button):
        pyautogui.moveTo(int(button[0]), int(button[1]), duration=0.2)

    def apply_click(self, button):
        pyautogui.mouseDown(int(button[0]), int(button[1]))
        time.sleep(0.2)
        pyautogui.mouseUp(int(button[0]), int(button[1]))
