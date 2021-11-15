import os
import unittest

import cv2

from app.core.templates import load_templates
from app.parsers.reborn_classic.farm.TargetHpParser import TargetHpParser
from app.parsers.reborn_classic.farm.TargetWindowParser import TargetWindowParser

env_path = os.path.dirname(os.path.realpath(__file__))


class TestParsers(unittest.TestCase):

    def setUp(self):
        self.templates = load_templates("res/template/interlude")

    def test_target_window_parser(self):
        parser = TargetWindowParser(env_path, self.templates.farm.target, debug=False)

        screen = cv2.imread("res/input/interlude/target/Shot00001.bmp")
        screen = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)
        assert len(screen) > 0

        result = parser.parse_image(screen)
        assert len(result) > 0
        return result

    def test_target_hp(self):
        parser = TargetHpParser(env_path, debug=True)
        result = parser.parse_image(self.test_target_window_parser())
        print(result)


if __name__ == '__main__':
    unittest.main()
