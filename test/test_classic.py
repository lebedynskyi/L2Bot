import unittest

import pytesseract

from src.parser.classic import ClassicTargetParser, ClassicNearTargetsParser, ClassicUserStatusParser
from src.template import ClassicTemplates
from test import read_input_img


class TestClassicNearestTargetsParser(unittest.TestCase):
    def setUp(self):
        self.parser = ClassicNearTargetsParser(debug=False)

    def test_parsing(self):
        rgb, grey = read_input_img("../res/input/classic/targets.bmp")

        result = self.parser.parse(rgb, grey)
        for r in result:
            print("%s distance -> %s" % (r.name, r.distance))
        print("----------------")

    def test_parsing1(self):
        rgb, grey = read_input_img("../res/input/classic/targets1.bmp")

        result = self.parser.parse(rgb, grey)
        for r in result:
            print("%s distance -> %s" % (r.name, r.distance))
        print("----------------")

    def test_parsing2(self):
        rgb, grey = read_input_img("../res/input/classic/targets2.bmp")

        result = self.parser.parse(rgb, grey)
        for r in result:
            print("%s distance -> %s" % (r.name, r.distance))
        print("----------------")


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
        rgb, grey = read_input_img("../res/input/classic/HP_46.bmp")
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


class TestClassicUserStatus(unittest.TestCase):
    def setUp(self):
        self.templates = ClassicTemplates("../res/templates")
        self.parser = ClassicUserStatusParser(self.templates, debug=False)

    def test_1(self):
        rgb, grey = read_input_img("../res/input/classic/Status_1.bmp")
        result = self.parser.parse(rgb, grey)
        assert result is not None
        # self.assertEqual((744, 744), result.cp)
        self.assertEqual((561, 1163), result.hp)
        # self.assertEqual((120, 295), result.mp)

    def test_2(self):
        rgb, grey = read_input_img("../res/input/classic/Status_2.bmp")
        result = self.parser.parse(rgb, grey)
        assert result is not None
        # self.assertEqual((249, 249), result.cp)
        self.assertEqual((336, 356), result.hp)
        # self.assertEqual((114, 114), result.mp)

    def test_3(self):
        rgb, grey = read_input_img("../res/input/classic/Status_3.bmp")
        result = self.parser.parse(rgb, grey)
        assert result is not None
        # self.assertEqual((249, 249), result.cp)
        self.assertEqual((356, 356), result.hp)
        # self.assertEqual((114, 114), result.mp)

    def test_4(self):
        rgb, grey = read_input_img("../res/input/classic/Status_4.bmp")
        result = self.parser.parse(rgb, grey)
        assert result is not None
        self.assertEqual((561, 1163), result.hp)

    def test_5(self):
        rgb, grey = read_input_img("../res/input/classic/Status_5.bmp")
        result = self.parser.parse(rgb, grey)
        assert result is not None
        self.assertEqual((995, 1289), result.hp)

    def test_6(self):
        rgb, grey = read_input_img("../res/input/classic/Status_6.bmp")
        result = self.parser.parse(rgb, grey)
        assert result is not None
        self.assertEqual((717, 1289), result.hp)

    def test_7(self):
        rgb, grey = read_input_img("../res/input/classic/Status_7.bmp")
        result = self.parser.parse(rgb, grey)
        assert result is not None
        self.assertEqual((650, 1289), result.hp)

    def test_8(self):
        rgb, grey = read_input_img("../res/input/classic/Status_8.bmp")
        result = self.parser.parse(rgb, grey)
        assert result is not None
        self.assertEqual((617, 1289), result.hp)

    def test_9(self):
        rgb, grey = read_input_img("../res/input/classic/Status_9.bmp")
        result = self.parser.parse(rgb, grey)
        assert result is not None
        self.assertEqual((584, 1289), result.hp)

    def test_10(self):
        rgb, grey = read_input_img("../res/input/classic/Status_10.bmp")
        result = self.parser.parse(rgb, grey)
        assert result is not None
        self.assertEqual((517, 1289), result.hp)

    def test_11(self):
        rgb, grey = read_input_img("../res/input/classic/Status_11.bmp")
        result = self.parser.parse(rgb, grey)
        assert result is not None
        self.assertEqual((483, 1289), result.hp)

    def test_12(self):
        rgb, grey = read_input_img("../res/input/classic/Status_12.bmp")
        result = self.parser.parse(rgb, grey)
        assert result is not None
        self.assertEqual((339, 1289), result.hp)

    def test_13(self):
        rgb, grey = read_input_img("../res/input/classic/Status_13.bmp")
        result = self.parser.parse(rgb, grey)
        assert result is not None
        self.assertEqual((276, 1289), result.hp)
