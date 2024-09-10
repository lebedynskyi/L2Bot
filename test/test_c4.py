import unittest

from src.parser.c4 import ManorC4Parser
from src.template import C4Templates
from test import read_input_img


class TestManorParser(unittest.TestCase):
    def setUp(self):
        templates = C4Templates("../res/templates")
        self.parser = ManorC4Parser(templates, True)

    def test_manor_window(self):
        rgb, grey = read_input_img("../res/input/c4/manor/window.bmp")

        result = self.parser.manor_window(grey)
        assert result
        assert result.exist

    def test_crop_list(self):
        rgb, grey = read_input_img("../res/input/c4/manor/crop_list.bmp")

        result = self.parser.crop_list(grey)
        assert result
        assert result.exist

    def test_crop_list2(self):
        rgb, grey = read_input_img("../res/input/c4/manor/crop_list2.bmp")

        result = self.parser.crop_list(grey)
        assert result
        assert result.exist

    def test_price_list(self):
        rgb, grey = read_input_img("../res/input/c4/manor/price_list.png")

        result = self.parser.price_list(grey)
        assert result
        assert result.exist
        assert result.ok_btn
        assert result.max_price_btn
        assert result.chooser_btn
