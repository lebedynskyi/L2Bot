import datetime
import unittest

from src.parser.c3 import C3NearTargetsParser, C3TargetParser
from src.template import C3Templates
from test.tools import read_input_img


class TestNearestTargets(unittest.TestCase):
    def setUp(self):
        self.parser = C3NearTargetsParser(debug=False)

    def test_parsing1(self):
        rgb, grey = read_input_img("../res/input/c3/Shot00004.bmp")

        print("Start %s\n" % datetime.datetime.now())
        result = self.parser.parse(rgb, grey)
        for r in result:
            print("%s distance -> %s" % (r.name, r.distance))
        print("\nFinish %s\n" % datetime.datetime.now())

    def test_parsing2(self):
        rgb, grey = read_input_img("../res/input/c3/Shot00008.bmp")

        print("Start %s\n" % datetime.datetime.now())
        result = self.parser.parse(rgb, grey)
        for r in result:
            print("%s distance -> %s" % (r.name, r.distance))
        print("\nFinish %s" % datetime.datetime.now())


class TestTarget(unittest.TestCase):
    def setUp(self):
        templates = C3Templates("../res/templates")
        self.parser = C3TargetParser(templates, debug=False)

    def test_parsing_5hp(self):
        rgb, grey = read_input_img("../res/input/c3/HP_5.bmp")
        result = self.parser.parse(rgb, grey)
        self.assertTrue(result.has_target)
        self.assertEqual(5, result.hp)

    def test_parsing_50hp(self):
        rgb, grey = read_input_img("../res/input/c3/HP_50.bmp")
        result = self.parser.parse(rgb, grey)
        self.assertTrue(result.has_target)
        self.assertEqual(50, result.hp)

    def test_parsing_78hp(self):
        rgb, grey = read_input_img("../res/input/c3/HP_78.bmp")
        result = self.parser.parse(rgb, grey)
        self.assertTrue(result.has_target)
        self.assertEqual(78 , result.hp)
