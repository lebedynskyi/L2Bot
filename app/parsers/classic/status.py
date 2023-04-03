import cv2
import numpy as np
from pytesseract import pytesseract

from app.parsers.base import BaseParser


class PetStatusParser(BaseParser):
    def __init__(self, output_path, pet_template, debug=False):
        super().__init__(output_path, debug)
        self.template = cv2.cvtColor(pet_template, cv2.COLOR_RGB2GRAY)

    def parse_image(self, screen_rgb, *args, **kwargs):
        hp, mp = None, None
        hp_rgb, mp_rgb = self.crop_areas(screen_rgb)
        if hp_rgb is not None:
            hp = self.parse_hp(hp_rgb)

        if mp_rgb is not None:
            mp = self.parse_mp(mp_rgb)

        return hp, mp

    def crop_areas(self, screen_rgb):
        image_rgb = screen_rgb.copy()
        image = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2GRAY)

        match = cv2.matchTemplate(image, self.template, cv2.TM_CCORR_NORMED)

        thresh_hold = 0.89
        loc = np.where(match >= thresh_hold)

        # draw matches
        match_points = list(zip(*loc[::-1]))
        if match_points:
            warn_pt = match_points[0]
            # all_square = ((warn_pt[0] + 18, warn_pt[1] + 26), (warn_pt[0] + 175, warn_pt[1] + 42))
            hp_square = ((warn_pt[0] + 18, warn_pt[1] + 26), (warn_pt[0] + 175, warn_pt[1] + 33))
            mp_square = ((warn_pt[0] + 18, warn_pt[1] + 33), (warn_pt[0] + 175, warn_pt[1] + 42))
            hp_square_rgb = screen_rgb[hp_square[0][1]:hp_square[1][1], hp_square[0][0]:hp_square[1][0]]
            mp_square_rgb = screen_rgb[mp_square[0][1]:mp_square[1][1], mp_square[0][0]:mp_square[1][0]]
            if self.debug:
                debug_img = image_rgb.copy()
                cv2.rectangle(debug_img, hp_square[0], hp_square[1], (0, 0, 255), 1)
                cv2.rectangle(debug_img, mp_square[0], mp_square[1], (0, 0, 255), 1)
                self.debug_show_im(debug_img, "Status template")
                self.debug_show_im(hp_square_rgb, "HP area")
                self.debug_show_im(mp_square_rgb, "MP area")
            return hp_square_rgb, mp_square_rgb
        return None, None

    def parse_hp(self, hp_area):
        hp_area = cv2.cvtColor(hp_area, cv2.COLOR_BGR2RGB)

        width = int(hp_area.shape[1] * 5)
        height = int(hp_area.shape[0] * 5)
        dim = (width, height)

        # resize image
        resized = cv2.resize(hp_area, dim, interpolation=cv2.INTER_AREA)
        if self.debug:
            self.debug_show_im(resized, "Resized target")

        # Color segmentation
        hsv = cv2.cvtColor(resized, cv2.COLOR_BGR2HSV)
        lower_red = np.array([0, 50, 70])  # 50 almostt best. need try 70
        upper_red = np.array([2, 255, 255])
        mask = cv2.inRange(hsv, lower_red, upper_red)
        res = cv2.bitwise_and(resized, resized, mask=mask)

        # Contour exctraction
        imgray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(imgray, (5, 5), 0)
        ret, thresholded = cv2.threshold(blurred, 50, 255, 0)
        contours, h = cv2.findContours(thresholded, 1, 2)

        if contours:
            cnt = contours[0]
            approx = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)
            if cv2.contourArea(cnt) > 25:  # to discard noise from the color segmentation
                contour_poly = cv2.approxPolyDP(cnt, 3, True)
                center, radius = cv2.minEnclosingCircle(contour_poly)

                if self.debug:
                    color = (0, 255, 0)
                    cv2.circle(resized, (int(center[0]), int(center[1])), int(radius), color, 2)
                    self.debug_show_im(resized, "Found limits")

                resized_width = int(resized.shape[1])
                hp_width = radius * 2

                return int(hp_width * 100 / resized_width)

        return -1

    def parse_mp(self, mp_area):
        mp_area = cv2.cvtColor(mp_area, cv2.COLOR_BGR2RGB)

        width = int(mp_area.shape[1] * 5)
        height = int(mp_area.shape[0] * 5)
        dim = (width, height)

        # resize image
        resized = cv2.resize(mp_area, dim, interpolation=cv2.INTER_AREA)
        if self.debug:
            self.debug_show_im(resized, "Resized target")

        # Color segmentation
        hsv = cv2.cvtColor(resized, cv2.COLOR_BGR2HSV)
        lower_blue = np.array([104, 202, 0])  # 50 almostt best. need try 70
        upper_blue = np.array([179, 255, 255])
        mask = cv2.inRange(hsv, lower_blue, upper_blue)
        res = cv2.bitwise_and(resized, resized, mask=mask)

        # Contour exctraction
        imgray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(imgray, (5, 5), 0)
        ret, thresholded = cv2.threshold(blurred, 50, 255, 0)
        contours, h = cv2.findContours(thresholded, 1, 2)

        if contours:
            cnt = contours[0]
            approx = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)
            if cv2.contourArea(cnt) > 25:  # to discard noise from the color segmentation
                contour_poly = cv2.approxPolyDP(cnt, 3, True)
                center, radius = cv2.minEnclosingCircle(contour_poly)

                if self.debug:
                    color = (0, 255, 0)
                    cv2.circle(resized, (int(center[0]), int(center[1])), int(radius), color, 2)
                    self.debug_show_im(resized, "Found limits")

                resized_width = int(resized.shape[1])
                mp_width = radius * 2

                return int(mp_width * 100 / resized_width)

        return -1


class FullStatusParser(BaseParser):
    def __init__(self, output_path, status_panel_template, debug=False):
        super().__init__(output_path, debug)
        self.hp_mp_template = status_panel_template

    def parse_image(self, screen_rgb, *args, **kwargs):
        hp_rgb = self.crop_hp(screen_rgb)
        if hp_rgb is not None:
            hp_text = self.extract_text(hp_rgb).replace(" ", "")
            return hp_text.split("/")
        return None

    def crop_hp(self, screen_rgb):
        image_rgb = screen_rgb.copy()
        image = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2GRAY)

        match = cv2.matchTemplate(image, self.hp_mp_template, cv2.TM_CCORR_NORMED)

        thresh_hold = 0.89
        loc = np.where(match >= thresh_hold)

        # draw matches
        hh, ww = self.hp_mp_template.shape[:2]
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

    def extract_text(self, text_area_rgb):
        gray = cv2.cvtColor(text_area_rgb, cv2.COLOR_RGB2GRAY)
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

        width = int(thresh.shape[1] * 900 / 100)
        height = int(thresh.shape[0] * 900 / 100)
        dim = (width, height)

        # resize image
        resized = cv2.resize(thresh, dim, interpolation=cv2.INTER_AREA)

        blur = cv2.GaussianBlur(resized, (21, 21), 0)
        if self.debug:
            self.debug_show_im(blur, "Debug blurred for text")

        tesseract_config = r"--oem 3 --psm 12 -l eng -c tessedit_char_whitelist=0123456789/"
        return pytesseract.image_to_string(blur, lang="eng", config=tesseract_config).strip()