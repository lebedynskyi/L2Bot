from abc import ABC

import cv2
import numpy as np
import pytesseract

from app.parsers.Base import BaseParser


class UserStatusParser(BaseParser):
    def __init__(self, env_path, status_template, debug=False):
        super().__init__(env_path, debug)
        self.template = cv2.cvtColor(status_template, cv2.COLOR_RGB2GRAY)

    def parse_image(self, screen_rgb):
        hp_rgb = self.crop_hp(screen_rgb)
        hp_text = self.extarct_text(hp_rgb)
        hp_coef = eval(hp_text)
        return hp_coef

    def crop_hp(self, screen_rgb):
        image_rgb = screen_rgb.copy()
        image = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2GRAY)

        match = cv2.matchTemplate(image, self.template, cv2.TM_CCORR_NORMED)

        thresh_hold = 0.89
        loc = np.where(match >= thresh_hold)

        # draw matches
        hh, ww = self.template.shape[:2]
        match_points = list(zip(*loc[::-1]))
        if match_points:
            warn_pt = match_points[0]
            hp_square = ((warn_pt[0] + 45, warn_pt[1] + 39), (warn_pt[0] + 150, warn_pt[1] + 52))
            hp_area_rgb = screen_rgb[hp_square[0][1]:hp_square[1][1], hp_square[0][0]:hp_square[1][0]]
            if self.debug:
                debug_img = image_rgb.copy()
                # self.draw_match_squares(debug_img, match_points, ww, hh)
                cv2.rectangle(debug_img, hp_square[0], hp_square[1], (0, 0, 255), 1)
                self.debug_show_im(debug_img, "Status template")
                self.debug_show_im(hp_area_rgb, "HP area")
            return hp_area_rgb
        return None

    def extarct_text(self, text_area_rgb):
        gray = cv2.cvtColor(text_area_rgb, cv2.COLOR_RGB2GRAY)
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

        width = int(thresh.shape[1] * 600 / 100)
        height = int(thresh.shape[0] * 600 / 100)
        dim = (width, height)

        # resize image
        resized = cv2.resize(thresh, dim, interpolation=cv2.INTER_AREA)

        blur = cv2.GaussianBlur(resized, (11, 11), 0)
        if self.debug:
            self.debug_show_im(blur, "Debug blurred for text")

        tesseract_config = r"--oem 3 --psm 11 -l eng -c tessedit_char_whitelist= 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789,.+-/='"
        text = pytesseract.image_to_string(blur, lang="eng", config=tesseract_config)
        print("Prsed text: text -> %s" % text)
        return text