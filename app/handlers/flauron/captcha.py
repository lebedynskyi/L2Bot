import cv2

from app.handlers.base import BaseHandler


class FlauronCaptchaHandler(BaseHandler):
    def __init__(self, solver, keyboard, dialog_parser, text_parser, quiz_start_parser, quiz_continue_parser):
        super().__init__(keyboard)
        self.dialog_parser = dialog_parser
        self.text_parser = text_parser
        self.captcha_solver = solver
        self.quiz_start_parser = quiz_start_parser
        self.quiz_continue_parser = quiz_continue_parser

    def _on_tick(self, screenshot_image, current_time, last_action_delta):
        answer = None
        if last_action_delta >= 1:
            self.last_action_time = current_time
            answer = self._check_dialog_captcha(screenshot_image)
            if not answer:
                answer = self._check_quiz_start(screenshot_image)

            if not answer:
                answer = self._check_quiz_continue(screenshot_image)

            if answer:
                self.keyboard.mouse_click(self.keyboard.KEY_MOUSE_LEFT, answer)

        return answer

    def _check_dialog_captcha(self, screenshot_image):
        dialog, ok_position, cancel_position = self.dialog_parser.parse_image(screenshot_image)
        if dialog is None:
            self.write_log("Captcha", "No Solo captcha")
            return

        for scale in range(500, 800, 100):
            try:
                captcha_text = self.text_parser.parse_image(dialog, default_scale=scale)
                result = self.captcha_solver.solve(captcha_text)

                cv2.imwrite("res/output/last_solved_captcha.png", screenshot_image)
                if result:
                    return ok_position
                else:
                    return cancel_position
            except BaseException as e:
                print("Cannot solve captcha, it was scale  %s " % scale)
                print(e)
                cv2.imwrite("res/output/last_error.png", screenshot_image)

    def _check_quiz_start(self, screenshot_image):
        result = self.quiz_start_parser.parse_image(screenshot_image)
        if not result:
            self.write_log("Captcha", "No Quiz start")

        return result

    def _check_quiz_continue(self, screenshot_image):
        result = self.quiz_continue_parser.parse_image(screenshot_image)
        if not result:
            self.write_log("Captcha", "No Quiz continue")

        return result
