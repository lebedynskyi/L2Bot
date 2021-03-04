import cv2
import numpy as np
import os
import pytesseract
import app.CVUtil as CVUtil
import imutils

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

        img = cv2.imread(input)
        dialog_template = cv2.imread(dialog_template)
        self._find_scaled1(img.copy(), dialog_template)

    def _find_scaled2(self, gray_image, gray_template):
        pass

    def _find_scaled1(self, gray_image, gray_template):
        tH, tW = gray_template.shape[:2]

        gray_image = cv2.GaussianBlur(gray_image, (1, 1), 0)
        gray_template = cv2.GaussianBlur(gray_template, (1, 1), 0)

        found = None
        for scale in np.linspace(0.2, 1.0, 20)[::-1]:
            resized = imutils.resize(gray_image, width=int(gray_image.shape[1] * scale))
            r = gray_image.shape[1] / float(resized.shape[1])

            if resized.shape[0] < tH or resized.shape[1] < tW:
                break

            edged = cv2.Canny(resized, 50, 200)
            result = cv2.matchTemplate(edged, gray_template, cv2.TM_CCORR_NORMED)
            (minVal, maxVal, _, maxLoc) = cv2.minMaxLoc(result)

            # if we have found a new maximum correlation value, then ipdate
            # the bookkeeping variable
            if found is None or maxVal > found[0]:
                found = (maxVal, maxLoc, r)

        (maxVal, maxLoc, r) = found
        # Threshold setting, this 11195548 value is tested by some random images
        threshold = 11195548
        if maxVal > threshold:
            (startX, startY) = (int(maxLoc[0] * r), int(maxLoc[1] * r))
            (endX, endY) = (int((maxLoc[0] + tW) * r), int((maxLoc[1] + tH) * r))

            # draw a bounding box around the detected result and display the image
            cv2.rectangle(gray_image, (startX, startY), (endX, endY), (0, 255, 0), 2)
            cv2.imshow("Image", gray_image)
            cv2.waitKey(0)
        else:
            print("no match found")

    def find_captcha_dialog(self, image, template):
        img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

        dialog_w, dialog_h = template.shape[::-1]
        res = CVUtil.match_template(img, template)
        threshold = 0.8
        loc = np.where(res >= threshold)
        dialog_points = list(zip(*loc[::-1]))
        if dialog_points:
            pt = dialog_points[0]
            dialog_img = img[pt[1]:pt[1] + dialog_h, pt[0]:pt[0] + dialog_w]
            cv2.imwrite('output/last_dialog.png', dialog_img)

            croppped = img[pt[1]:pt[1] + 58, pt[0] + 30:pt[0] + dialog_w]

            thresh = cv2.threshold(croppped, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

            scale_percent = 400  # percent of original size
            width = int(croppped.shape[1] * scale_percent / 100)
            height = int(croppped.shape[0] * scale_percent / 100)
            dim = (width, height)

            # resize image
            resized = cv2.resize(thresh, dim, interpolation=cv2.INTER_AREA)

            blurred = cv2.GaussianBlur(resized, (11, 11), 0)

            captcha_text_image = blurred
            cv2.imwrite('output/last_captcha_box.png', captcha_text_image)

            # tesseract_config = r"--oem 3 --psm 11 -c tessedit_char_whitelist= 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789,.'"
            # text = pytesseract.image_to_string(captcha_text_image, lang="eng", config=tesseract_config)
            # print("Captcha text -> %s" % text)
            return True
        return False
