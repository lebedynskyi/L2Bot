import cv2 as cv
import numpy as np
import os
import pytesseract
import app.CVUtil as CVUtil

from pytesseract import Output
from matplotlib import pyplot as plt


class AntiBotParser:
    def __init__(self):
        pass

    def parse(self, input, dialog_template):
        if not os.path.exists(input):
            raise FileNotFoundError(input)

        if not os.path.exists(dialog_template):
            raise FileNotFoundError(dialog_template)

        print("Parsing file -> %s" % input)

        img = cv.imread(input, cv.IMREAD_GRAYSCALE)
        dialog_template = cv.imread(dialog_template, cv.IMREAD_GRAYSCALE)
        self._find_captcha_dialog(img.copy(), dialog_template)

    def _find_captcha_dialog(self, gray_image, gray_template):
        img = gray_image.copy()
        dialog_w, dialog_h = gray_template.shape[::-1]

        res = CVUtil.match_template(img, gray_template)
        threshold = 0.8
        loc = np.where(res >= threshold)
        dialog_points = list(zip(*loc[::-1]))
        if not dialog_points:
            print("No dialog found")
            return False
        else:
            print("Found captcha dialog")
            pt = dialog_points[0]
            dialog_img = img[pt[1]:pt[1] + dialog_h, pt[0]:pt[0] + dialog_w]
            cv.imwrite('dialog.png', dialog_img)

            croppped = img[pt[1]:pt[1] + 58, pt[0] + 30:pt[0] + dialog_w]

            thresh = cv.threshold(croppped, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)[1]

            scale_percent = 400  # percent of original size
            width = int(croppped.shape[1] * scale_percent / 100)
            height = int(croppped.shape[0] * scale_percent / 100)
            dim = (width, height)

            # resize image
            resized = cv.resize(thresh, dim, interpolation=cv.INTER_AREA)

            blurred = cv.GaussianBlur(resized, (11, 11), 0)

            captcha_text_image = blurred
            cv.imwrite('working.png', captcha_text_image)

            tesseract_config = r"--oem 3 --psm 11 -c tessedit_char_whitelist= 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789,.'"
            text = pytesseract.image_to_string(captcha_text_image, lang="eng", config=tesseract_config)
            print("Captcha text -> %s" % text)
            return True

            # plt.title('Detected dialog'), plt.xticks([]), plt.yticks([])
            # plt.imshow(dialog_img, cmap="gray")
            # plt.show()

            # cv.imshow("Detected dialog", dialog_img)
            # cv.waitKey(0)
