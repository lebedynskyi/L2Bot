import os
import unittest

import cv2

from app.core.templates import load_templates
from app.parsers.classic.target import TargetHpParser
from app.parsers.classic.target import TargetWindowParser

env_path = os.path.dirname(os.path.realpath(__file__))


class TestParsers(unittest.TestCase):

    def setUp(self):
        self.templates = load_templates("res/template/classic")

    def test_target_window_parser(self):
        parser = TargetWindowParser(env_path, self.templates.farm.target, debug=False)

        screen = cv2.imread("res/input/classic/target/Shot00002.bmp")
        assert len(screen) > 0

        result = parser.parse_image(screen)
        assert result is not None and len(result) > 0
        return result

    def test_target_hp(self):
        screen = cv2.imread("res/input/classic/target/Shot00005.bmp")
        window_parser = TargetWindowParser(env_path, self.templates.farm.target, debug=False)
        parser = TargetHpParser(env_path, debug=False)
        hp_box = window_parser.parse_image(screen)
        result = parser.parse_image(hp_box)
        print(result)


if __name__ == '__main__':
    unittest.main()
