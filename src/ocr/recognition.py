import logging
import os
from abc import ABC, abstractmethod

import cv2
import pytesseract

logger = logging.getLogger("Recognition")
os.environ['OMP_THREAD_LIMIT'] = '1'


class Recognition(ABC):
    i = 0

    @abstractmethod
    def extract(self, img_grey, scale):
        pass

    def parse_text(self, img_grey, scale, whitelist):
        try:
            thresh = cv2.threshold(img_grey, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

            height = int(thresh.shape[0] * scale)
            width = int(thresh.shape[1] * scale)
            dim = (width, height)

            # resize image
            resized = cv2.resize(thresh, dim, interpolation=cv2.INTER_AREA)
            blur = cv2.GaussianBlur(resized, (5, 5), 0)

            # cv2.imwrite("%s.png" % self.i, blur)
            # self.i = self.i + 1

            # cv2.imshow("blurred", blur)
            # cv2.waitKey(0)

            tesseract_config = r"--oem 3 --psm 10 -l eng -c tessedit_char_whitelist=%s" % whitelist
            text = pytesseract.image_to_string(blur, config=tesseract_config)
            logger.debug("Parsed text is -> '%s'", text)
            return text
        except BaseException as e:
            logger.warning("Unable to parse text, %s", e)
        return None


class NumbersRecognition(Recognition):
    def extract(self, img_grey, scale):
        text = self.parse_text(img_grey, scale, "0123456789")
        try:
            return int(text.strip())
        except:
            pass

        return None


class TextRecognition(Recognition):
    def extract(self, img_grey, scale):
        text = self.parse_text(img_grey, scale, "")
        if text:
            return text.strip()
        return None
