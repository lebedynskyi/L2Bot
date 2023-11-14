import datetime
import unittest

from src.parser.c3 import C3NearTargetsParser, C3TargetParser
from src.template import C3Templates
from test import read_input_img


class TestNearestTargetsParser(unittest.TestCase):
    def setUp(self):
        self.parser = C3NearTargetsParser(debug=False)

    def test_parsing1(self):
        rgb, grey = read_input_img("../res/input/c3/Shot00004.bmp")

        print("Start %s" % datetime.datetime.now())
        result = self.parser.parse(rgb, grey)
        for r in result:
            print("%s distance -> %s" % (r.name, r.distance))
        print("Finish %s\n\n" % datetime.datetime.now())

    def test_parsing2(self):
        rgb, grey = read_input_img("../res/input/c3/Shot00008.bmp")

        print("Start %s" % datetime.datetime.now())
        result = self.parser.parse(rgb, grey)
        for r in result:
            print("%s distance -> %s" % (r.name, r.distance))
        print("Finish %s\n\n" % datetime.datetime.now())


class TestC3TargetParser(unittest.TestCase):
    def setUp(self):
        templates = C3Templates("../res/templates")
        self.parser = C3TargetParser(templates, debug=False)

    def test_parsing_6hp(self):
        rgb, grey = read_input_img("../res/input/c3/HP_5.bmp")
        result = self.parser.parse(rgb, grey)
        self.assertTrue(result.exist)
        self.assertEqual(6, result.hp)

    def test_parsing_52hp(self):
        rgb, grey = read_input_img("../res/input/c3/HP_50.bmp")
        result = self.parser.parse(rgb, grey)
        self.assertTrue(result.exist)
        self.assertEqual(52, result.hp)

    def test_parsing_81hp(self):
        rgb, grey = read_input_img("../res/input/c3/HP_78.bmp")
        result = self.parser.parse(rgb, grey)
        self.assertTrue(result.exist)
        self.assertEqual(81, result.hp)

    def test_parsing_100hp(self):
        rgb, grey = read_input_img("../res/input/c3/HP_100.bmp")
        result = self.parser.parse(rgb, grey)
        self.assertTrue(result.exist)
        self.assertEqual(99, result.hp)

    def test_parsing_0hp(self):
        rgb, grey = read_input_img("../res/input/c3/HP_0.bmp")
        result = self.parser.parse(rgb, grey)
        self.assertTrue(result.exist)
        self.assertEqual(0, result.hp)
