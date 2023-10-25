import unittest

from src.parser.classic import ClassicTargetParser
from src.template import ClassicTemplates
from test.tools import read_input_img


class TestClassicTargetParser(unittest.TestCase):
    def setUp(self):
        self.templates = ClassicTemplates("../res/templates")
        self.parser = ClassicTargetParser(self.templates, debug=False)

    def test_hp_0(self):
        rgb, grey = read_input_img("../res/input/classic/HP_0.bmp")
        result = self.parser.parse(rgb, grey)
        assert result is not None
        self.assertTrue(result.exist)
        self.assertEqual(0, result.hp)

    def test_hp_45(self):
        rgb, grey = read_input_img("../res/input/classic/HP_45.bmp")
        result = self.parser.parse(rgb, grey)
        assert result is not None
        self.assertTrue(result.exist)
        self.assertEqual(45, result.hp)

    def test_hp_72(self):
        rgb, grey = read_input_img("../res/input/classic/HP_75.bmp")
        result = self.parser.parse(rgb, grey)
        assert result is not None
        self.assertTrue(result.exist)
        self.assertEqual(72, result.hp)

    def test_hp_100(self):
        rgb, grey = read_input_img("../res/input/classic/HP_100.bmp")
        result = self.parser.parse(rgb, grey)
        assert result is not None
        self.assertTrue(result.exist)
        self.assertEqual(99, result.hp)
