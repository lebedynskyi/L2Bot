import os
import unittest

import cv2

from app.core.templates import load_templates
from app.parsers.farm.TargetWindowParser import TargetWindowParser


class TestParsers(unittest.TestCase):
    env_path = os.path.dirname(os.path.realpath(__file__))

    def setUp(self):
        self.templates = load_templates("res/template/interlude")

    def test_target_hp(self):
        pass

    def test_target_window_parser(self):
        parser = TargetWindowParser(self.env_path, self.templates.farm.target, debug=True)

        screen = cv2.imread("res/input/interlude/target/Screen60.jpeg")
        assert screen

        result = parser.parse_image(screen)
        assert result
