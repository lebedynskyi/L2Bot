import unittest

import pytesseract


class TestDependencies(unittest.TestCase):
    def test_tesseract(self):
        lng = pytesseract.get_languages()
        assert len(lng) > 0
