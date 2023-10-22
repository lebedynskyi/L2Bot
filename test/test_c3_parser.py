import datetime
import unittest

from src.parser.c3 import C3NearTargetsParser
from test.base import read_input_img


class TestNearestTargets(unittest.TestCase):
    def setUp(self):
        self.parser = C3NearTargetsParser(debug=False)

    def test_parsing1(self):
        rgb, grey = read_input_img("res/input/c3/Shot00004.bmp")

        print("Start %s\n" % datetime.datetime.now())
        result = self.parser.parse(rgb, grey)
        for r in result:
            print("%s distance -> %s" % (r.name, r.distance))
        print("\nFinish %s\n" % datetime.datetime.now())

    def test_parsing2(self):
        rgb, grey = read_input_img("res/input/c3/Shot00008.bmp")

        print("Start %s\n" % datetime.datetime.now())
        result = self.parser.parse(rgb, grey)
        for r in result:
            print("%s distance -> %s" % (r.name, r.distance))
        print("\nFinish %s" % datetime.datetime.now())


if __name__ == "__main__":
    unittest.main()
