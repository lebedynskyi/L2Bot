import os
import time

import cv2
import pyautogui

from app.Loigic import Logic
# from app.Ui import Ui
# from app.WarningPlayer import WarningPlayer
from app.WarningPlayer import WarningPlayer
from app.parsers.WarnDialog import WarnDialogParser
from app.parsers.Captcha import CaptchaParser
from app.solver.CaptchaSolver import CaptchaSolver

env_path = os.path.dirname(os.path.realpath(__file__))


def test_dialog_warn():
    warn_template = cv2.imread("res/template/warning_template.png")
    screen = cv2.imread("input/screens/Yes1.bmp")

    dialog_handler = WarnDialogParser(env_path, warn_template)
    dialog, ok, cancel = dialog_handler.parse_image(screen)
    pyautogui.moveTo(ok[0], ok[1])
    WarningPlayer(os.path.join("res/warn.mp3")).play_captcha()


def test_loop():
    warn_template = cv2.imread("res/template/warning_template.png")
    dialog_parser = WarnDialogParser(env_path, warn_template)
    captcha_parser = CaptchaParser(env_path)
    captcha_solver = CaptchaSolver()
    logic = Logic(dialog_parser, captcha_parser, captcha_solver)

    while True:
        btn = logic.check_captcha()
        if btn is not None:
            logic.apply_click(btn)
        time.sleep(2)


def test_captcha_parser():
    import cv2

    warn_template = cv2.imread("res/template/warning_template.png")
    screen = cv2.imread("input/screens/Shot00006.bmp")

    dialog_handler = WarnDialogParser(env_path, warn_template)
    captcha_handler = CaptchaParser(env_path, dialog_handler, False)

    solver = CaptchaSolver()
    for f in os.listdir("input/screens"):
        print("----------------------------------------")
        print(f)
        img = cv2.imread(os.path.join("input/screens", f))
        captcha_text = captcha_handler.parse_image(img)
        if captcha_text:
            is_math = solver.is_ariphmetic(captcha_text)
            if is_math:
                print("Captcha: Math captcha")
                math_answer = solver.solve_math(captcha_text)
                if math_answer:
                    print("Captcha: Result is OK")
                else:
                    print("Captcha: Result is Cancel")
            else:
                print("Captcha: Logic captcha")
                logic_answer = solver.solve_logic(captcha_text)
                if logic_answer:
                    print("Captcha: Result is OK")
                else:
                    print("Captcha: Result is Cancel")
        else:
            print("Captcha: No found")


if __name__ == "__main__":
    test_dialog_warn()
    # test_loop()

    # warn_template = cv2.imread("res/template/warning_template.png")
    # dialog_parser = WarnDialogParser(env_path, warn_template)
    # captcha_parser = CaptchaParser(env_path)
    # captcha_solver = CaptchaSolver()
    # captcha_player = WarningPlayer(os.path.join("res/warn.mp3"))
    #
    # icon_path = os.path.join(env_path, "res/app_ico.png")
    #
    # app = Ui("Captcha", icon_path, captcha_player, Logic(dialog_parser, captcha_parser, captcha_solver))
    # app.start_ui()
