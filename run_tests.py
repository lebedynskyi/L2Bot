import os
import time
import unittest

import cv2

from app.core.controls import MockKeyboard
from app.core.templates import load_templates
from app.handlers.Manor import ManorSellCastle, ManorHandler
from app.parsers.classic.manor import ManorDialogParser, CropListParser, CastlesListParser, CastlesListChooserParser

env_path = os.path.dirname(os.path.realpath(__file__))


#
# class TestParsers(unittest.TestCase):
#
#     def setUp(self):
#         self.templates = load_templates("res/template/classic")
#
#     def test_target_window_parser(self):
#         parser = TargetWindowParser(env_path, self.templates.farm.target, debug=False)
#
#         screen = cv2.imread("res/input/classic/target/Shot00002.bmp")
#         assert len(screen) > 0
#
#         result = parser.parse_image(screen)
#         assert result is not None and len(result) > 0
#         return result
#
#     def test_target_hp(self):
#         screen = cv2.imread("res/input/classic/target/Shot00005.bmp")
#         window_parser = TargetWindowParser(env_path, self.templates.farm.target, debug=False)
#         parser = TargetHpParser(env_path, debug=False)
#         hp_box = window_parser.parse_image(screen)
#         result = parser.parse_image(hp_box)
#         print(result)


# class TestSoloCaptcha(unittest.TestCase):
#     def setUp(self):
#         self.templates = load_templates("res/template/classic")
#
#     def test_warn_dialog(self):
#         screen = cv2.imread("res/input/classic/captcha/Shot00008.bmp")
#         dialog_parser = WarnDialogParser(env_path, self.templates.captcha.warn_dialog, debug=False)
#         dialog, ok_position, cancel_position = dialog_parser.parse_image(screen)
#
#         captcha_parser = DialogTextParser(env_path, debug=False)
#         captcha_text = captcha_parser.parse_image(dialog, default_scale=500)
#         print(captcha_text)
#
#         solver = CaptchaSolver()
#         print(solver.solve_math(captcha_text))


class TestManor(unittest.TestCase):
    def setUp(self):
        self.templates = load_templates("res/template/classic")
        self.keyboard = MockKeyboard()

    def test_manor(self):
        castles = [
            ManorSellCastle("Gludio", "Fake", start_index=2)
            # ManorSellCastle("Giran", "Fake", start_index=3)
        ]

        manor_dialog_parser = ManorDialogParser(env_path, self.templates.manor.manor_dialog_template)
        crop_list_parser = CropListParser(env_path, self.templates.manor.crop_sales_dialog, True)
        castles_list_parser = CastlesListParser(env_path, self.templates.manor.chooser_template)
        castles_chooser_parser = CastlesListChooserParser(env_path, self.templates.manor.chooser_expanded_template)
        manor = ManorHandler(self.keyboard, castles,
                             manor_dialog_parser, crop_list_parser, castles_list_parser, castles_chooser_parser)

        screen1 = cv2.imread("res/input/classic/manor/Shot00016.bmp")
        screen2 = cv2.imread("res/input/classic/manor/Shot00017.bmp")
        screen3 = cv2.imread("res/input/classic/manor/Shot00018.bmp")
        screen4 = cv2.imread("res/input/classic/manor/Shot00019.bmp")
        manor.on_tick(screen1, time.time())
        manor.on_tick(screen2, time.time())
        manor.on_tick(screen3, time.time())
        manor.on_tick(screen4, time.time())


if __name__ == '__main__':
    unittest.main()
