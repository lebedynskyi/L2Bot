import time
import os
import cv2

from app.logic.ManorLogic import ManorLogic, SellCastle
from app.parsers.captcha.GroupDialogParser import GroupDialogParser
from app.parsers.captcha.WarnDialog import WarnDialogParser
from app.parsers.manor.CastlesListChooserParser import CastlesListChooserParser
from app.parsers.manor.CastlesListParser import CastlesListParser
from app.parsers.manor.CropListParser import CropListParser
from app.parsers.manor.ManorDialogParser import ManorDialogParser
from app.parsers.status.UserDeathStatusParser import UserDeathStatusParser
from app.parsers.status.UserStatusParser import UserStatusParser

env_path = os.path.dirname(os.path.realpath(__file__))


def get_files_from_folder(folder_path):
    files = []
    for filename in os.scandir(folder_path):
        if filename.is_file() and "bmp" in filename.name:
            files.append(filename.path)
    return sorted(files)


def test_dialog_warn():
    warn_template = cv2.imread("res/template/warning_template.png")
    screen = cv2.imread("input/screens/Yes1.bmp")

    dialog_handler = WarnDialogParser(env_path, warn_template)
    dialog, ok, cancel = dialog_handler.parse_image(screen)
    assert dialog
    assert ok
    assert cancel


def test_status_parser():
    status_template = cv2.imread("res/template/status/user_status_template.png")
    status_parser = UserStatusParser(env_path, status_template, True)

    screen = cv2.imread("input/screens/Shot00008.bmp")
    assert status_parser.parse_image(screen)


def test_tesseract():
    import pytesseract

    lng = pytesseract.get_languages()
    print(lng)


def test_dualbox_parser():
    warn_template = cv2.imread("res/template/dualbox_template.png")
    screen = cv2.imread("input/group/Shot00011.bmp")

    dualbox_handler = GroupDialogParser(env_path, warn_template, False)
    assert dualbox_handler.parse_image(screen)


def test_status_parser(screen_shots):
    from app.parsers.status.UserStatusParser import UserStatusParser

    status_template = cv2.imread("res/template/status/user_status_template.png")
    status_parser = UserStatusParser(env_path, status_template, debug=True)
    for shot in screen_shots:
        image = cv2.imread(shot)
        hp_coef = status_parser.parse_image(image)
        print("{} -> {}".format(shot, hp_coef))


def test_death_parser():
    status_template = cv2.imread("res/template/status/user_death_template.png")
    status_parser = UserDeathStatusParser(env_path, status_template, True)

    screen = cv2.imread("input/screens/Shot00037.bmp")
    assert status_parser.parse_image(screen)


def test_manor_logic(screen_shots):
    castles = [SellCastle("Aden", "Fake", 2, 4, 2)]

    manor_dialog_template = cv2.imread("res/template/manor/manor_template_1.png")
    manor_dialog_parser = ManorDialogParser(env_path, manor_dialog_template, debug=True)

    crop_list_template = cv2.imread("res/template/manor/crop_sales_dialog.png")
    crop_list_parser = CropListParser(env_path, crop_list_template, debug=True)

    castles_list_template = cv2.imread("res/template/manor/chooser_template.png")
    castles_list_parser = CastlesListParser(env_path, castles_list_template, debug=True)

    castles_chooser_parser_template = cv2.imread("res/template/manor/chooser_expanded_template.png")
    castles_chooser_parser = CastlesListChooserParser(env_path, castles_chooser_parser_template, debug=True)

    manor = ManorLogic(castles, manor_dialog_parser, crop_list_parser, castles_list_parser, castles_chooser_parser)

    for shot in screen_shots:
        image = cv2.imread(shot)
        print("ManorTest: check image -> {}".format(shot))
        manor.on_tick(image, time.time())


if __name__ == "__main__":
    # screens = get_files_from_folder("input/screens")
    # test_status_parser(screens)

    # manor_screens = get_files_from_folder("input/manor")
    # test_manor_logic(manor_screens)

    pass