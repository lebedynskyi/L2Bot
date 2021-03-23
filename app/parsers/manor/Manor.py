from datetime import datetime

import cv2
import numpy as np
from pytesseract import pytesseract

from app.parsers.Base import BaseParser

MANOR_DIALOG = 0
CROP_SALES = 1
CHOOSER_COLLAPSED = 2
CHOOSER_EXPANDED = 3
MAX_PRICE = 4
MAX_PRICE_OK = 5
SELL = 6
FINISH = 7


class ManorParser(BaseParser):
    current_stadia = MANOR_DIALOG

    cached_max_price = None
    cached_max_price_ok = None
    cached_crop_sale = None
    cached_chooser_dialog = None
    next_castle = None
    current_castle_index = 0

    def __init__(self, output_path, interested_castles, manor_template, crop_sales_template, chooser_template,
                 debug=False):
        super().__init__(output_path, debug)
        self.interested_castles = interested_castles
        self.next_castle = interested_castles[self.current_castle_index]
        self.crop_sales_template = cv2.cvtColor(crop_sales_template, cv2.COLOR_RGB2GRAY)
        self.manor_template = cv2.cvtColor(manor_template, cv2.COLOR_RGB2GRAY)
        self.chooser_template = cv2.cvtColor(chooser_template, cv2.COLOR_RGB2GRAY)

    def parse_image(self, screen_rgb):
        if self.current_stadia == MANOR_DIALOG:
            return self.handle_manor_dialog(screen_rgb)
        elif self.current_stadia == CROP_SALES:
            return self.handle_crop_sales(screen_rgb)
        elif self.current_stadia == CHOOSER_COLLAPSED:
            return self.handle_chooser_collapses(screen_rgb)
        elif self.current_stadia == CHOOSER_EXPANDED:
            return self.handle_chooser_expanded(screen_rgb)
        elif self.current_stadia == MAX_PRICE:
            return self.handle_max_price()
        elif self.current_stadia == MAX_PRICE_OK:
            return self.handle_max_price_ok()
        elif self.current_stadia == SELL:
            return self.handle_sell()
        elif self.current_stadia == FINISH:
            raise KeyboardInterrupt()
        return None

    def handle_manor_dialog(self, screen_rgb):
        print("Manor: %s Look for Manor dialog" % datetime.now())
        image_rgb = screen_rgb.copy()
        image = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2GRAY)
        match = cv2.matchTemplate(image, self.manor_template, cv2.TM_CCORR_NORMED)
        thresh_hold = 0.89
        loc = np.where(match >= thresh_hold)
        hh, ww = self.manor_template.shape[:2]
        # Match could have more than 1 item

        match_points = list(zip(*loc[::-1]))
        if match_points:
            first_points = match_points[0]
            sale_btn = ((first_points[0] + 535, first_points[1] + 275), (first_points[0] + 550, first_points[1] + 290))
            print("Manor: %s Found Manor dialog" % datetime.now())

            if self.debug:
                debug_img = screen_rgb.copy()
                self.draw_match_squares(debug_img, match_points, ww, hh)
                cv2.rectangle(debug_img, sale_btn[0], sale_btn[1], (0, 0, 255), 1)
                self.debug_show_im(debug_img)

            sell_x = (sale_btn[0][0] + sale_btn[1][0]) / 2
            sell_y = (sale_btn[1][1] + sale_btn[0][1]) / 2
            self.current_stadia = self.current_stadia + 1
            return sell_x, sell_y
        print("Manor: Manor not found")
        return None

    def handle_crop_sales(self, screen_rgb):
        print("Manor: %s Look for crops dialog" % datetime.now())
        image_rgb = screen_rgb.copy()
        image = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2GRAY)
        match = cv2.matchTemplate(image, self.crop_sales_template, cv2.TM_CCORR_NORMED)
        thresh_hold = 0.89
        loc = np.where(match >= thresh_hold)
        hh, ww = self.crop_sales_template.shape[:2]
        # Match could have more than 1 item

        match_points = list(zip(*loc[::-1]))
        if match_points:
            first_match = match_points[0]
            self.cached_crop_sale = (
            (first_match[0] + 470, first_match[1] + 5), (first_match[0] + 485, first_match[1] + 20))
            seed_row = ((first_match[0] + 50, first_match[1] - 187), (first_match[0] + 65, first_match[1] - 202))
            print("Manor: %s Found crops dialog" % datetime.now())

            if self.debug:
                debug_img = screen_rgb.copy()
                self.draw_match_squares(debug_img, match_points, ww, hh)
                cv2.rectangle(debug_img, seed_row[0], seed_row[1], (0, 0, 255), 1)
                cv2.rectangle(debug_img, self.cached_crop_sale[0], self.cached_crop_sale[1], (0, 0, 255), 1)
                self.debug_show_im(debug_img)

            # Todo Return double click in row
            seed_x = (seed_row[0][0] + seed_row[1][0]) / 2
            seed_y = (seed_row[1][1] + seed_row[0][1]) / 2
            self.current_stadia = self.current_stadia + 1
            return seed_x, seed_y
        print("Manor: Crops not found")
        return None

    def handle_chooser_collapses(self, screen_rgb):
        print("Manor: %s Look chooser dialog" % datetime.now())
        image_rgb = screen_rgb.copy()
        image = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2GRAY)
        match = cv2.matchTemplate(image, self.chooser_template, cv2.TM_CCORR_NORMED)
        thresh_hold = 0.89
        loc = np.where(match >= thresh_hold)
        hh, ww = self.chooser_template.shape[:2]
        # Match could have more than 1 item

        match_points = list(zip(*loc[::-1]))
        if match_points:
            first_match = match_points[0]
            self.cached_chooser_dialog = first_match
            select_btn = ((first_match[0] + 150, first_match[1] + 122), (first_match[0] + 165, first_match[1] + 137))
            self.cached_max_price_ok = (
            (first_match[0] + 112, first_match[1] + 187), (first_match[0] + 127, first_match[1] + 202))
            self.cached_max_price = (
            (first_match[0] + 210, first_match[1] + 150), (first_match[0] + 230, first_match[1] + 165))

            print("Manor: %s Found chooser dialog" % datetime.now())
            if self.debug:
                debug_img = screen_rgb.copy()
                self.draw_match_squares(debug_img, match_points, ww, hh)
                cv2.rectangle(debug_img, select_btn[0], select_btn[1], (0, 0, 255), 1)
                cv2.rectangle(debug_img, self.cached_max_price_ok[0], self.cached_max_price_ok[1], (0, 0, 255), 1)
                cv2.rectangle(debug_img, self.cached_max_price[0], self.cached_max_price[1], (0, 0, 255), 1)
                self.debug_show_im(debug_img, "Collapsed dialog")

            select_x = (select_btn[0][0] + select_btn[1][0]) / 2
            select_y = (select_btn[1][1] + select_btn[0][1]) / 2
            self.current_stadia = self.current_stadia + 1
            return select_x, select_y
        print("Manor: Chooser not found")
        return None

    def handle_chooser_expanded(self, screen_rgb):
        print("Manor: %s Look for castles dialog" % datetime.now())

        if self.cached_chooser_dialog:
            first_match = self.cached_chooser_dialog

            for i in range(2, 8):
                print("Manor: %s Look for castles name" % datetime.now())
                castle = (
                    # 17 pixels height per 1 castle
                    (first_match[0] + 116, first_match[1] + 122 + i * 17),
                    (first_match[0] + 255, first_match[1] + 122 + i * 17 + 17)
                )

                castle_name = self._parse_castle(screen_rgb, castle)
                print("Manor: %s Castle name %s" % (datetime.now(), castle_name))
                if self.next_castle in castle_name:
                    self.current_stadia = self.current_stadia + 1
                    castle_x = (castle[0][0] + castle[1][0]) / 2
                    castle_y = (castle[1][1] + castle[0][1]) / 2
                    print("Manor: %s Found interested castle -> %s" % (datetime.now(), castle_name))
                    return castle_x, castle_y

        print("Manor: Castles not found")
        return None

    def handle_max_price(self):
        x = (self.cached_max_price[0][0] + self.cached_max_price[1][0]) / 2
        y = (self.cached_max_price[1][1] + self.cached_max_price[0][1]) / 2
        self.current_stadia = self.current_stadia + 1
        return x, y

    def handle_max_price_ok(self):
        x = (self.cached_max_price_ok[0][0] + self.cached_max_price_ok[1][0]) / 2
        y = (self.cached_max_price_ok[1][1] + self.cached_max_price_ok[0][1]) / 2
        self.current_stadia = self.current_stadia + 1
        return x, y

    def handle_sell(self):
        x = (self.cached_crop_sale[0][0] + self.cached_crop_sale[1][0]) / 2
        y = (self.cached_crop_sale[1][1] + self.cached_crop_sale[0][1]) / 2
        print("Manor: %s Sold" % datetime.now())

        next_index = self.current_castle_index + 1
        if next_index < len(self.interested_castles):
            self.current_castle_index = next_index
            self.current_stadia = MANOR_DIALOG
            self.next_castle = self.interested_castles[self.current_castle_index]
        else:
            self.current_stadia = FINISH
        return x, y

    def _parse_castle(self, screen_rgb, castle_area):
        # dialog_rgb[5:60, 34:300]
        castle_img = screen_rgb[castle_area[0][1]:castle_area[1][1], castle_area[0][0]:castle_area[1][0]]
        gray = cv2.cvtColor(castle_img, cv2.COLOR_RGB2GRAY)
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

        tesseract_config = r"--oem 3 --psm 7 -l eng -c tessedit_char_whitelist= 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789,.+-/='"
        text = pytesseract.image_to_string(blur, lang="eng", config=tesseract_config)
        return text
