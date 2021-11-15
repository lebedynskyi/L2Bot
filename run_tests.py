import os
import unittest

import cv2

from app.core.templates import load_templates
from app.parsers.classic.target import TargetHpParser
from app.parsers.classic.target import TargetWindowParser
from app.parsers.reborn_classic.ui import WarnDialogParser
from app.parsers.text import DialogTextParser
from app.solver.CaptchaSolver import CaptchaSolver

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


class TestSoloCaptcha(unittest.TestCase):
    def setUp(self):
        self.templates = load_templates("res/template/classic")

    def test_warn_dialog(self):
        screen = cv2.imread("res/input/classic/captcha/Shot00008.bmp")
        dialog_parser = WarnDialogParser(env_path, self.templates.captcha.warn_dialog, debug=False)
        dialog, ok_position, cancel_position = dialog_parser.parse_image(screen)

        captcha_parser = DialogTextParser(env_path, debug=False)
        captcha_text = captcha_parser.parse_image(dialog, default_scale=500)
        print(captcha_text)

        solver = CaptchaSolver()
        print(solver.solve_math(captcha_text))



if __name__ == '__main__':
    unittest.main()
