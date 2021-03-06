import os

from app.handlers.WarnDialogHandler import WarnDialogHandler

env_path = os.path.dirname(os.path.realpath(__file__))


def test_dialog_warn():
    import cv2

    template = cv2.imread("res/template/warning_template.png")
    dialog_match = WarnDialogHandler(env_path, template, True)

    screen = cv2.imread("input/Yes1.bmp")
    dialog_match.parse_image(screen)


if __name__ == "__main__":
    test_dialog_warn()

    # icon_path = os.path.join(env_path, "res/app_ico.png")
    # app = App("Captcha", icon_path, env_path, WarningPlayer(os.path.join("res/captcha_warn_long.wav")))
    # app.run()
