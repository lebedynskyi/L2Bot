import datetime
import os
import time

import cv2
import pyautogui

from app.logic.CaptchaLoigic import CaptchaLogic
# from app.logic.UserDeathLogic import UserDeathLogic
from app.logic.UserStatusLogic import UserStatusLogic
from app.parsers.status.UserDeathStatusParser import UserDeathStatusParser
from app.parsers.status.UserStatusParser import UserStatusParser
from app.parsers.manor import Manor
from app.logic.ManorLogic import ManorLogic
from app.parsers.captcha.GroupDialogParser import GroupDialogParser
from app.parsers.captcha.WarnDialog import WarnDialogParser
from app.parsers.captcha.BotCaptcha import BotCaptchaParser
from app.solver.CaptchaSolver import CaptchaSolver

env_path = os.path.dirname(os.path.realpath(__file__))

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.02


def test_dialog_warn():
    warn_template = cv2.imread("res/template/warning_template.png")
    screen = cv2.imread("input/screens/Yes1.bmp")

    dialog_handler = WarnDialogParser(env_path, warn_template)
    dialog, ok, cancel = dialog_handler.parse_image(screen)
    pyautogui.moveTo(ok[0], ok[1])

def test_status_parser():
    status_template = cv2.imread("res/template/status/user_status_template.png")
    status_parser = UserStatusParser(env_path, status_template, True)

    screen = cv2.imread("input/screens/Shot00008.bmp")
    status_parser.parse_image(screen)


def test_loop():
    warn_template = cv2.imread("res/template/warning_template.png")
    group_template = cv2.imread("res/template/dualbox_template.png")

    dialog_parser = WarnDialogParser(env_path, warn_template)
    captcha_parser = BotCaptchaParser(env_path)
    group_parser = GroupDialogParser(env_path, group_template)
    captcha_solver = CaptchaSolver()
    logic = CaptchaLogic(dialog_parser, captcha_parser, group_parser, captcha_solver, None)

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


def run_manor_app():
    manor_templ = cv2.imread("res/template/manor/manor_template_1.png")
    crop_sales_templ = cv2.imread("res/template/manor/crop_sales_dialog.png")
    chooser_templ = cv2.imread("res/template/manor/chooser_template.png")
    chooser_expanded_templ = cv2.imread("res/template/manor/chooser_expanded_template.png")

    # Parse start from 0. Position 2 means first castle.
    # Desert Codran - Goddard
    manor_parser = Manor.ManorParser(env_path, [
        Manor.CastleLookArea("Aden", "fake", 4, 7),
        Manor.CastleLookArea("Goddard", "fake", 4, 7)
    ], manor_templ, crop_sales_templ, chooser_templ, chooser_expanded_templ, False)
    logic = ManorLogic(manor_parser)

    time.sleep(4)

    # check_time()
    while True:
        btn = logic.check_manor()
        if btn is not None:
            logic.apply_move(btn)
            logic.apply_click(btn)
            if logic.manor_parser.current_stadia == Manor.CHOOSER_COLLAPSED:
                logic.apply_click(btn)
        elif logic.manor_parser.current_stadia == Manor.CROP_SALES:
            # Manor in maintenance mode
            time.sleep(0.1)
            logic.apply_click()


def check_time():
    current_time = datetime.datetime.now()
    if current_time.hour < 23 or current_time.minute < 5 or current_time.second < 45:
        print("Manor Loop: wait for 23 hours 5 min 45 sec")
        time.sleep(4)


def test_manor():
    manor_templ = cv2.imread("res/template/manor/manor_template_1.png")
    crop_sales_templ = cv2.imread("res/template/manor/crop_sales_dialog.png")
    chooser_templ = cv2.imread("res/template/manor/chooser_template.png")
    chooser_expanded_templ = cv2.imread("res/template/manor/chooser_expanded_template.png")
    manor_parser = Manor.ManorParser(env_path,
                                     [
                                         Manor.CastleLookArea("Aden", start_index=2)
                                         # Manor.CastleLookArea("Dion", start_index=4)
                                     ], manor_templ, crop_sales_templ, chooser_templ, chooser_expanded_templ, True)

    manor_screen = cv2.imread("input/manor/Shot00023.bmp")
    crop_sales_screen = cv2.imread("input/manor/Shot00024.bmp")
    chooser_screen = cv2.imread("input/manor/Shot00021.bmp")
    chooser_exp_screen = cv2.imread("input/manor/Shot00022.bmp")

    # First
    manor_parser.parse_image(manor_screen)
    manor_parser.parse_image(crop_sales_screen)
    manor_parser.parse_image(chooser_screen)
    manor_parser.parse_image(chooser_exp_screen)
    manor_parser.parse_image(chooser_screen)
    manor_parser.parse_image(chooser_screen)
    manor_parser.parse_image(crop_sales_screen)

    # Second

    manor_parser.parse_image(manor_screen)
    manor_parser.parse_image(crop_sales_screen)
    manor_parser.parse_image(chooser_screen)
    manor_parser.parse_image(chooser_exp_screen)
    manor_parser.parse_image(chooser_screen)
    manor_parser.parse_image(chooser_screen)
    manor_parser.parse_image(crop_sales_screen)


def test_captcha_parser():
    import cv2

    warn_template = cv2.imread("res/template/warning_template.png")
    dialog_handler = WarnDialogParser(env_path, warn_template, True)
    captcha_handler = BotCaptchaParser(env_path, True)

    solver = CaptchaSolver()
    for f in os.listdir("input/screens"):
        print("----------------------------------------")
        print(f)
        img = cv2.imread(os.path.join("input/screens", f))
        touple = dialog_handler.parse_image(img)
        if touple[0] is None:
            print("No dialog found")
            continue

        for scale in range(500, 800, 100):
            captcha_text = captcha_handler.parse_image(touple[0], scale)
            try:
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
                break
            except:
                print("Cannot solve captcha at all, text %s, scale %s" % (captcha_text, scale))


# Works in Windows only
def run_captcha_app():
    from app.Ui import Ui

    warn_template = cv2.imread("res/template/warning_template.png")
    group_template = cv2.imread("res/template/dualbox_template.png")
    status_template = cv2.imread("res/template/status/user_status_template.png")
    death_template = cv2.imread("res/template/status/user_death_template.png")


    dialog_parser = WarnDialogParser(env_path, warn_template)
    captcha_parser = BotCaptchaParser(env_path)
    group_captcha_parser = GroupDialogParser(env_path, group_template)
    user_status_parser = UserStatusParser(env_path, status_template)
    user_death_parser = UserDeathStatusParser(env_path, death_template)

    captcha_solver = CaptchaSolver()

    icon_path = os.path.join(env_path, "res/app_ico.png")

    app = Ui("Antlbt", icon_path,
             CaptchaLogic(dialog_parser, captcha_parser, group_captcha_parser, captcha_solver),
             UserStatusLogic(user_status_parser),
             UserDeathLogic(user_death_parser))
    app.start_ui()


def test_death_parser():
    status_template = cv2.imread("res/template/status/user_death_template.png")
    status_parser = UserDeathStatusParser(env_path, status_template, True)

    screen = cv2.imread("input/screens/Shot00037.bmp")
    status_parser.parse_image(screen)


if __name__ == "__main__":
    # test_dialog_warn()
    # test_loop()
    # test_status_parser()
    # test_captcha_parser()
    # test_tesseract()
    # test_player()
    # test_dualbox()
    # test_death_parser()
    #
    # test_manor()


    run_manor_app()
    # run_captcha_app()
