import cv2

from app.handlers.BaseHandler import BaseHandler, apply_click


class CaptchaHandler(BaseHandler):
    def __init__(self, keyboard, dialog_parser, captcha_parser, group_parser, captcha_solver):
        super().__init__(keyboard)
        self.dialog_parser = dialog_parser
        self.captcha_parser = captcha_parser
        self.captcha_solver = captcha_solver
        self.group_parser = group_parser

    def _on_tick(self, screenshot_image, current_time, last_action_delta):
        answer = None
        if last_action_delta >= 1:
            self.last_action_time = current_time
            answer = self._check_anti_bot_captcha(screenshot_image)
            if not answer:
                answer = self._check_group_captcha(screenshot_image)

            if answer:
                apply_click(answer)

        return answer

    def _check_anti_bot_captcha(self, screenshot_image):
        dialog, ok_position, cancel_position = self.dialog_parser.parse_image(screenshot_image)
        if dialog is None:
            self.write_log("Captcha", "No Solo captcha")
            return

        for scale in range(500, 800, 100):
            try:
                captcha_text = self.captcha_parser.parse_image(dialog, default_scale=scale)
                if self.captcha_solver.is_ariphmetic(captcha_text):
                    result = self.captcha_solver.solve_math(captcha_text)
                else:
                    result = self.captcha_solver.solve_logic(captcha_text)
                cv2.imwrite("res/output/last_solved_captcha.png", screenshot_image)
                if result:
                    return ok_position
                else:
                    return cancel_position
            except BaseException as e:
                print("Cannot solve captcha, it was scale  %s " % scale)
                print(e)
                cv2.imwrite("res/output/last_error.png", screenshot_image)

    def _check_group_captcha(self, screenshot_image):
        result = self.group_parser.parse_image(screenshot_image)
        if not result:
            self.write_log("Captcha", "No Group captcha")

        return result
