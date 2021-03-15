import os
import time

import cv2
import pyautogui

from app.BotCaptchaLoigic import Logic
from app.Ui import Ui
from app.WarningPlayer import WarningPlayer
from app.parsers.GroupDialogParser import GroupDialogParser
from app.parsers.WarnDialog import WarnDialogParser
from app.parsers.BotCaptcha import BotCaptchaParser
from app.solver.CaptchaSolver import CaptchaSolver

env_path = os.path.dirname(os.path.realpath(__file__))


def test_dialog_warn():
    warn_template = cv2.imread("res/template/warning_template.png")
    screen = cv2.imread("input/screens/Yes1.bmp")

    dialog_handler = WarnDialogParser(env_path, warn_template)
    dialog, ok, cancel = dialog_handler.parse_image(screen)
    pyautogui.moveTo(ok[0], ok[1])


def test_player():
    player = WarningPlayer("res/captcha_warn_short.wav",
                           os.path.join(env_path, "res", "captcha_warn_long.wav"))
    player.play_captcha()
    time.sleep(2)


def test_loop():
    warn_template = cv2.imread("res/template/warning_template.png")
    group_template = cv2.imread("res/template/dualbox_template.png")

    dialog_parser = WarnDialogParser(env_path, warn_template)
    captcha_parser = BotCaptchaParser(env_path)
    group_parser = GroupDialogParser(env_path, group_template)
    captcha_solver = CaptchaSolver()
    logic = Logic(dialog_parser, captcha_parser, group_parser, captcha_solver, None)

    while True:
        btn = logic.check_captcha()
        if btn is not None:
            logic.apply_move(btn)
            time.sleep(1)
            logic.apply_click(btn)
        time.sleep(2)


def test_tesseract():
    import pytesseract

    lng = pytesseract.get_languages()
    print(lng)


def test_dualbox():
    warn_template = cv2.imread("res/template/dualbox_template.png")
    screen = cv2.imread("input/group/Shot00011.bmp")

    dualbox_handler = GroupDialogParser(env_path, warn_template, True)
    result = dualbox_handler.parse_image(screen)


def test_captcha_parser():
    import cv2

    warn_template = cv2.imread("res/template/warning_template.png")
    dialog_handler = WarnDialogParser(env_path, warn_template, False)
    captcha_handler = BotCaptchaParser(env_path, False)

    solver = CaptchaSolver()
    for f in os.listdir("input/screens"):
        print("----------------------------------------")
        print(f)
        img = cv2.imread(os.path.join("input/screens", f))
        touple = dialog_handler.parse_image(img)
        if touple[0] is None:
            print("No dialog found")
            continue

        captcha_text = captcha_handler.parse_image(touple[0])
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
    # test_dialog_warn()
    # test_loop()
    # test_captcha_parser()
    # test_tesseract()
    # test_player()

    # test_dualbox()

    warn_template = cv2.imread("res/template/warning_template.png")
    group_template = cv2.imread("res/template/dualbox_template.png")

    dialog_parser = WarnDialogParser(env_path, warn_template)
    captcha_parser = BotCaptchaParser(env_path)
    captcha_solver = CaptchaSolver()
    group_parser = GroupDialogParser(env_path, group_template)

    captcha_player = WarningPlayer("res/captcha_warn_short.wav", "res/captcha_warn_long.wav")

    icon_path = os.path.join(env_path, "res/app_ico.png")

    app = Ui("Antlbt", icon_path, Logic(dialog_parser, captcha_parser, group_parser, captcha_solver, captcha_player))
    app.start_ui()
