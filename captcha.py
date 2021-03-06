import os

from app.parsers.WarnDialog import WarnDialogParser
from app.parsers.Captcha import CaptchaParser

env_path = os.path.dirname(os.path.realpath(__file__))


def test_dialog_warn():
    import cv2

    warn_template = cv2.imread("res/template/warning_template.png")
    screen = cv2.imread("input/Yes1.bmp")

    dialog_handler = WarnDialogParser(env_path, warn_template)
    dialog_handler.parse_image(screen)


def test_captcha_parser():
    import cv2

    warn_template = cv2.imread("res/template/warning_template.png")
    screen = cv2.imread("input/Yes4.bmp")

    dialog_handler = WarnDialogParser(env_path, warn_template)
    captcha_handler = CaptchaParser(env_path, dialog_handler)
    captcha_handler.parse_image(screen)


if __name__ == "__main__":
    test_captcha_parser()

    # icon_path = os.path.join(env_path, "res/app_ico.png")
    # app = App("Captcha", icon_path, env_path, WarningPlayer(os.path.join("res/captcha_warn_long.wav")))
    # app.run()
