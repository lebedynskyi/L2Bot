import os
import time

from app.core.controls import ArduinoKeyboard, SoftKeyboard
import app.core.templates as templates
from app.core.looper import AppLooper
from app.handlers.captcha import CaptchaHandler
from app.handlers.flauron.captcha import FlauronCaptchaHandler
from app.parsers.flauron.ui import WarnDialogParser, QuizStartDialogParser, QuizContinueDialogParser
from app.parsers.text import TextParser
from app.solver.CaptchaSolver import CaptchaSolver

env_path = os.path.dirname(os.path.realpath(__file__))


def farm_app():
    keyboard = SoftKeyboard()
    keyboard.init(0.1)

    template = templates.load_templates("res/template/reborn_classic")
    warn_dialog_parser = WarnDialogParser(env_path, template.captcha.warn_dialog)
    quiz_start_dialog_parser = QuizStartDialogParser(env_path, template.captcha.captcha_quiz_start)
    quiz_continue_parser = QuizContinueDialogParser(env_path, template.captcha.captcha_quiz_continue)
    solver = CaptchaSolver()
    dialog_text_parser = TextParser(env_path)
    captcha_h = FlauronCaptchaHandler(solver, keyboard, warn_dialog_parser, dialog_text_parser,
                                      quiz_start_dialog_parser, quiz_continue_parser)
    return AppLooper(captcha_h)


if __name__ == "__main__":
    time.sleep(1)
    farm_app().loop()
