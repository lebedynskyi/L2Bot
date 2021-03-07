import os

from app.parsers.WarnDialog import WarnDialogParser
from app.parsers.Captcha import CaptchaParser
from app.solver.CaptchaSolver import CaptchaSolver

env_path = os.path.dirname(os.path.realpath(__file__))


def test_dialog_warn():
    import cv2

    warn_template = cv2.imread("res/template/warning_template.png")
    screen = cv2.imread("input/screens/Yes1.bmp")

    dialog_handler = WarnDialogParser(env_path, warn_template)
    dialog_handler.parse_image(screen)


def test_captcha_parser():
    import cv2

    warn_template = cv2.imread("res/template/warning_template.png")
    screen = cv2.imread("input/screens/Shot00006.bmp")

    dialog_handler = WarnDialogParser(env_path, warn_template)
    captcha_handler = CaptchaParser(env_path, dialog_handler, False)

    solver = CaptchaSolver()
    for f in os.listdir("input/screens"):
        print("----------------------------------------")
        img = cv2.imread(os.path.join("input/screens", f))
        captcha_text = captcha_handler.parse_image(img)
        if captcha_text:
            is_math = solver.is_ariphmetic(captcha_text)
            if is_math:
                print("Captcha: Math captcha")
                solver.solve_math(captcha_text)
            else:
                print("Captcha: Logic captcha")
                solver.solve_logic(captcha_text)
        else:
            print("Captcha: No found")



if __name__ == "__main__":
    test_captcha_parser()

    # icon_path = os.path.join(env_path, "res/app_ico.png")
    # app = App("Captcha", icon_path, env_path, WarningPlayer(os.path.join("res/captcha_warn_long.wav")))
    # app.run()
