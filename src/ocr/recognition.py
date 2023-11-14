import logging
import os
from abc import ABC, abstractmethod

import cv2
import pytesseract

logger = logging.getLogger("Recognition")
os.environ['OMP_THREAD_LIMIT'] = '1'


class Recognition(ABC):
    i = 0
    oem = 3
    psm = 12

    @abstractmethod
    def extract(self, img_grey, scale, whitelist=""):
        pass

    def parse_text(self, img_grey, scale, whitelist):
        try:
            thresh = cv2.threshold(img_grey, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

            height = int(thresh.shape[0] * scale)
            width = int(thresh.shape[1] * scale)
            dim = (width, height)

            resized = cv2.resize(thresh, dim, interpolation=cv2.INTER_AREA)
            blur = cv2.GaussianBlur(resized, (5, 5), 0)

            # cv2.imshow("blurred", blur)
            # cv2.waitKey(0)

            tes_config = r"--oem %s --psm %s -l eng -c tessedit_char_whitelist=%s" % (self.oem, self.psm, whitelist)
            text = pytesseract.image_to_string(blur, config=tes_config)
            return text
        except BaseException as e:
            logger.warning("Unable to parse text -> %s", e)
        return None


class NumbersRecognition(Recognition):
    def extract(self, img_grey, scale, whitelist="0123456789"):
        text = None
        try:
            text = self.parse_text(img_grey, scale, whitelist)
            logger.debug("Parsed text is -> '%s'", text)
            return int(text.strip())
        except BaseException as e:
            logger.debug("Cannot parse int, text is '%s'", text)
        return None


class TextRecognition(Recognition):
    def extract(self, img_grey, scale, whitelist=""):
        try:
            text = self.parse_text(img_grey, scale, whitelist)
            logger.debug("Parsed text is -> '%s'", text)
            if text:
                return text.strip()
        except BaseException as e:
            pass

        return None
