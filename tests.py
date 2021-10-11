import os
import time
import unittest

import cv2
import pytesseract

from app.handlers.Manor import ManorSellCastle, ManorHandler
from app.parsers.captcha.GroupDialogParser import GroupDialogParser
from app.parsers.captcha.WarnDialog import WarnDialogParser
from app.parsers.farm.TemplateExistParser import TemplateExistParser
from app.parsers.manor.CastlesListChooserParser import CastlesListChooserParser
from app.parsers.manor.CastlesListParser import CastlesListParser
from app.parsers.manor.CropListParser import CropListParser
from app.parsers.manor.ManorDialogParser import ManorDialogParser
from app.parsers.status.UserDeathStatusParser import UserDeathStatusParser
from app.parsers.status.UserStatusParser import UserStatusParser

env_path = os.path.dirname(os.path.realpath(__file__))


def list_files(folder_path):
    files = []
    for filename in os.scandir(folder_path):
        if filename.is_file() and "bmp" in filename.name:
            files.append(filename.path)
    return sorted(files)


class TestDependencies(unittest.TestCase):
    def test_tesseract(self):
        lng = pytesseract.get_languages()
        assert len(lng) > 0


class TestHandlers(unittest.TestCase):
    def test_manor_handler(self):
        screen_shots = list_files("res/input/manor")
        castles = [ManorSellCastle("Aden", "Fake", 2, 4, 2)]

        manor_dialog_template = cv2.imread("res/template/manor/manor_template_1.png")
        manor_dialog_parser = ManorDialogParser(env_path, manor_dialog_template)

        crop_list_template = cv2.imread("res/template/manor/crop_sales_dialog.png")
        crop_list_parser = CropListParser(env_path, crop_list_template)

        castles_list_template = cv2.imread("res/template/manor/chooser_template.png")
        castles_list_parser = CastlesListParser(env_path, castles_list_template)

        castles_chooser_parser_template = cv2.imread("res/template/manor/chooser_expanded_template.png")
        castles_chooser_parser = CastlesListChooserParser(env_path, castles_chooser_parser_template)

        manor = ManorHandler(castles, manor_dialog_parser, crop_list_parser, castles_list_parser,
                             castles_chooser_parser)

        for shot in screen_shots:
            image = cv2.imread(shot)
            print("ManorTest: check image -> {}".format(shot))
            manor.on_tick(image, time.time())


class TestParsers(unittest.TestCase):
    def test_status_parser(self):
        status_template = cv2.imread("res/template/status/user_status_template.png")
        status_parser = UserStatusParser(env_path, status_template)

        screen = cv2.imread("res/input/screens/Shot00008.bmp")
        assert status_parser.parse_image(screen)

    def test_target_parser(self):
        target_template = cv2.imread("res/template/farm/target_template.png")
        parser = TemplateExistParser(env_path, target_template)
        screen = cv2.imread("res/input/farm/Shot00055.bmp")
        assert parser.parse_image(screen)

    def test_dialog_warn(self):
        warn_template = cv2.imread("res/template/warning_template.png")
        screen = cv2.imread("res/input/screens/Yes1.bmp")

        dialog_handler = WarnDialogParser(env_path, warn_template)
        dialog, ok, cancel = dialog_handler.parse_image(screen)
        assert dialog is not None
        assert ok
        assert cancel

    def test_dualbox_parser(self):
        warn_template = cv2.imread("res/template/dualbox_template.png")
        screen = cv2.imread("res/input/group/Shot00011.bmp")

        group_captcha_parser = GroupDialogParser(env_path, warn_template)
        assert group_captcha_parser.parse_image(screen)

    def test_death_parser(self):
        status_template = cv2.imread("res/template/status/user_death_template.png")
        status_parser = UserDeathStatusParser(env_path, status_template )

        screen = cv2.imread("res/input/screens/Shot00037.bmp")
        assert status_parser.parse_image(screen)


if __name__ == '__main__':
    unittest.main()
