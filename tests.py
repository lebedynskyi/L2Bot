import os
import cv2

env_path = os.path.dirname(os.path.realpath(__file__))


def test_status_parser(screen_shots):
    from app.parsers.status.UserStatusParser import UserStatusParser

    status_template = cv2.imread("res/template/status/user_status_template.png")
    status_parser = UserStatusParser(env_path, status_template, debug=False)
    for shot in screen_shots:
        image = cv2.imread(shot)
        hp_coef = status_parser.parse_image(image)
        print("{} -> {}".format(shot, hp_coef))


if __name__ == "__main__":
    screens = []
    for filename in os.scandir("input/screens"):
        if filename.is_file() and "bmp" in filename.name:
            screens.append(filename.path)

    test_status_parser(screens)
