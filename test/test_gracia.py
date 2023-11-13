import unittest

from src.parser.gracia import GraciaFishing, GraciaTargetParser
from src.template import GraciaRebornTemplates
from test import read_input_img


class TestGraciaFishingParser(unittest.TestCase):
    def setUp(self):
        self.templates = GraciaRebornTemplates("../res/templates")
        self.parser = GraciaFishing(self.templates, debug=False)

    def test_fishing_dialog_exist(self):
        rgb, grey = read_input_img("../res/input/gracia/fishing/fish1.bmp")
        result = self.parser.parse(rgb, grey)
        assert result is not None
        self.assertTrue(True, result.is_fishing)

    def test_fishing_dialog_not_exist(self):
        rgb, grey = read_input_img("../res/input/gracia/fishing/fish0.png")
        result = self.parser.parse(rgb, grey)
        assert result is not None
        assert not result.is_fishing

    def test_fishing_26_seconds(self):
        rgb, grey = read_input_img("../res/input/gracia/fishing/fish4.bmp")
        result = self.parser.parse(rgb, grey)
        self.assertTrue(result is not None)
        self.assertEqual(26, result.seconds_left)

    def test_fishing_27_seconds(self):
        rgb, grey = read_input_img("../res/input/gracia/fishing/fish2.bmp")
        result = self.parser.parse(rgb, grey)
        assert result is not None
        self.assertEqual(27, result.seconds_left)

    def test_fishing_24_seconds(self):
        rgb, grey = read_input_img("../res/input/gracia/fishing/fish5.bmp")
        result = self.parser.parse(rgb, grey)
        assert result is not None

        self.assertEqual(24, result.seconds_left, )

    def test_fishing_21_seconds(self):
        rgb, grey = read_input_img("../res/input/gracia/fishing/fish6.bmp")
        result = self.parser.parse(rgb, grey)
        assert result is not None
        self.assertEqual(21, result.seconds_left)

    def test_fishing_23_hp(self):
        rgb, grey = read_input_img("../res/input/gracia/fishing/fish4.bmp")
        result = self.parser.parse(rgb, grey)
        self.assertTrue(result is not None)
        self.assertEqual(23, result.hp_percent)

    def test_fishing_60_hp(self):
        rgb, grey = read_input_img("../res/input/gracia/fishing/fish2.bmp")
        result = self.parser.parse(rgb, grey)
        assert result is not None
        self.assertEqual(60, result.hp_percent)

    def test_fishing_16_hp(self):
        rgb, grey = read_input_img("../res/input/gracia/fishing/fish5.bmp")
        result = self.parser.parse(rgb, grey)
        assert result is not None

        self.assertEqual(16, result.hp_percent, )

    def test_fishing_11_hp(self):
        rgb, grey = read_input_img("../res/input/gracia/fishing/fish6.bmp")
        result = self.parser.parse(rgb, grey)
        assert result is not None
        self.assertEqual(11, result.hp_percent)


class TestGraciaTargetParser(unittest.TestCase):
    def setUp(self):
        self.templates = GraciaRebornTemplates("../res/templates")
        self.parser = GraciaTargetParser(self.templates, debug=False)

    def test_hp_5(self):
        rgb, grey = read_input_img("../res/input/gracia/HP_4.bmp")
        result = self.parser.parse(rgb, grey)
        assert result is not None
        self.assertTrue(result.exist)
        self.assertEqual(5, result.hp)

    def test_hp_66(self):
        rgb, grey = read_input_img("../res/input/gracia/HP_70.bmp")
        result = self.parser.parse(rgb, grey)
        assert result is not None
        self.assertTrue(result.exist)
        self.assertEqual(66, result.hp)

    def test_hp_100(self):
        rgb, grey = read_input_img("../res/input/gracia/HP_100.bmp")
        result = self.parser.parse(rgb, grey)
        assert result is not None
        self.assertTrue(result.exist)
        self.assertEqual(99, result.hp)
