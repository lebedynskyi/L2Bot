from app.parsers.Base import BaseParser

import cv2
import pytesseract


class CaptchaParser(BaseParser):
    def __init__(self, env_path, warn_dialog_handler, debug=False):
        super().__init__(env_path, debug)
        self.warn_dialog_handler = warn_dialog_handler

    def parse_image(self, image):
        warn_dialog = self.warn_dialog_handler.parse_image(image)

        if warn_dialog is not None:
            text_area = self.crop_text_area(warn_dialog)
            return self.parse_text(text_area)
        return None

    def crop_text_area(self, dialog_rgb):
        text_area_rgb = dialog_rgb[5:60, 34:300]
        if self.debug:
            self.debug_show_im(text_area_rgb, "Debug Text area")
        return text_area_rgb

    def parse_text(self, text_area_rgb):
        gray = cv2.cvtColor(text_area_rgb, cv2.COLOR_RGB2GRAY)
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

        scale_percent = 500  # percent of original size
        width = int(thresh.shape[1] * scale_percent / 100)
        height = int(thresh.shape[0] * scale_percent / 100)
        dim = (width, height)

        # resize image
        resized = cv2.resize(thresh, dim, interpolation=cv2.INTER_AREA)

        blur = cv2.GaussianBlur(resized, (5, 5), 0)
        if self.debug:
            self.debug_show_im(blur, "Debug blurred for text")

        tesseract_config = r"--oem 3 --psm 11 -c tessedit_char_whitelist= 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789,.+-/='"
        text = pytesseract.image_to_string(blur, lang="eng", config=tesseract_config)
        print("Captcha: text -> %s" % text)
        return text
