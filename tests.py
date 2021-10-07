import time
import os
import cv2

from app.logic.ManorLogicNew import ManorLogicNew, SellCastle
from app.parsers.manor.CastlesListChooserParser import CastlesListChooserParser
from app.parsers.manor.CastlesListParser import CastlesListParser
from app.parsers.manor.CropListParser import CropListParser
from app.parsers.manor.ManorDialogParser import ManorDialogParser

env_path = os.path.dirname(os.path.realpath(__file__))


def get_files_from_folder(folder_path):
    files = []
    for filename in os.scandir(folder_path):
        if filename.is_file() and "bmp" in filename.name:
            files.append(filename.path)
    return sorted(files)


def test_status_parser(screen_shots):
    from app.parsers.status.UserStatusParser import UserStatusParser

    status_template = cv2.imread("res/template/status/user_status_template.png")
    status_parser = UserStatusParser(env_path, status_template, debug=True)
    for shot in screen_shots:
        image = cv2.imread(shot)
        hp_coef = status_parser.parse_image(image)
        print("{} -> {}".format(shot, hp_coef))


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

    manor = ManorLogicNew(castles, manor_dialog_parser, crop_list_parser, castles_list_parser, castles_chooser_parser)

    for shot in screen_shots:
        image = cv2.imread(shot)
        print("ManorTest: check image -> {}".format(shot))
        manor.on_tick(image, time.time())


if __name__ == "__main__":
    # screens = get_files_from_folder("input/screens")
    # test_status_parser(screens)

    manor_screens = get_files_from_folder("input/manor")
    test_manor_logic(manor_screens)
