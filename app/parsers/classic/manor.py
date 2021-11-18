from datetime import datetime

import cv2
import numpy as np
import pytesseract

from app.parsers.base import BaseParser


class CastlesListChooserParser(BaseParser):

    def __init__(self, output_path, list_chooser_template, debug=False):
        super().__init__(output_path, debug)
        self.list_chooser_template = cv2.cvtColor(list_chooser_template, cv2.COLOR_RGB2GRAY)

    def parse_image(self, image_rgb, *args, **kwargs):
        looking_castle = kwargs["castle"]

        image_rgb = image_rgb.copy()
        image = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2GRAY)
        match = cv2.matchTemplate(image, self.list_chooser_template, cv2.TM_CCORR_NORMED)

        loc = np.where(match >= 0.89)
        match_points = list(zip(*loc[::-1]))

        castle_x = None
        castle_y = None

        if match_points:
            first_match = match_points[0]

            if self.debug:
                hh, ww = self.list_chooser_template.shape[:2]
                debug_img = image_rgb.copy()
                self.draw_match_squares(debug_img, match_points, ww, hh)
                self.debug_show_im(debug_img, "Castle chooser")

            if looking_castle.castle_number < 2:
                print("Manor: look for castle {}".format(looking_castle.castle_name))
                for i in range(looking_castle.start_index, looking_castle.finish_index):
                    castle = (
                        # 17 pixels height per 1 castle
                        # (first_match[0] + 116, first_match[1] + 122 + i * 17),
                        # (first_match[0] + 255, first_match[1] + 122 + i * 17 + 17)
                        (first_match[0], first_match[1] + i * 17),
                        (first_match[0] + 140, first_match[1] + i * 17 + 17)
                    )

                    castle_name_string = self._parse_castle_name(image_rgb, castle)
                    if looking_castle.alternative_castle_name is not None and looking_castle.alternative_castle_name in castle_name_string:
                        castle_x = (castle[0][0] + castle[1][0]) / 2
                        castle_y = (castle[1][1] + castle[0][1]) / 2

                    if looking_castle.castle_name in castle_name_string:
                        castle_x = (castle[0][0] + castle[1][0]) / 2
                        castle_y = (castle[1][1] + castle[0][1]) / 2
                        break

            else:
                print("Manor: Use castle position {}".format(looking_castle.castle_number))
                castle = (
                    (first_match[0], first_match[1] + looking_castle.castle_number * 17),
                    (first_match[0] + 140, first_match[1] + looking_castle.castle_number * 17 + 17)
                )
                castle_x = (castle[0][0] + castle[1][0]) / 2
                castle_y = (castle[1][1] + castle[0][1]) / 2

        if castle_y is not None and castle_y is not None:
            return castle_x, castle_y

        print("Manor: Castles not found")
        return None

    def _parse_castle_name(self, screen_rgb, castle_area):
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

        blur = cv2.GaussianBlur(resized, (7, 7), 0)
        if self.debug:
            self.debug_show_im(blur, "Debug blurred for text")

        tesseract_config = r"--oem 3 --psm 7 -l eng -c tessedit_char_whitelist= 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'"
        text = pytesseract.image_to_string(blur, lang="eng", config=tesseract_config)
        return text


class CastlesListParser(BaseParser):
    def __init__(self, output_path, castles_list_template, debug=False):
        super().__init__(output_path, debug)
        self.castles_list_template = cv2.cvtColor(castles_list_template, cv2.COLOR_RGB2GRAY)

    def parse_image(self, image_rgb, *args, **kwargs):
        image_rgb = image_rgb.copy()
        image = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2GRAY)
        match = cv2.matchTemplate(image, self.castles_list_template, cv2.TM_CCORR_NORMED)

        loc = np.where(match >= 0.89)
        match_points = list(zip(*loc[::-1]))

        if match_points:
            first_match = match_points[0]

            drop_down_btn = ((first_match[0] + 240, first_match[1] + 125), (first_match[0] + 255, first_match[1] + 140))
            max_price_ok = ((first_match[0] + 112, first_match[1] + 187), (first_match[0] + 127, first_match[1] + 202))
            max_price = ((first_match[0] + 210, first_match[1] + 150), (first_match[0] + 230, first_match[1] + 165))

            if self.debug:
                debug_img = image_rgb.copy()
                hh, ww = self.castles_list_template.shape[:2]
                self.draw_match_squares(debug_img, match_points, ww, hh)
                cv2.rectangle(debug_img, drop_down_btn[0], drop_down_btn[1], (0, 255, 0), 1)
                cv2.rectangle(debug_img, max_price_ok[0], max_price_ok[1], (0, 0, 255), 1)
                cv2.rectangle(debug_img, max_price[0], max_price[1], (255, 0, 0), 1)
                self.debug_show_im(debug_img, "Collapsed dialog")

            select_x = (drop_down_btn[0][0] + drop_down_btn[1][0]) / 2
            select_y = (drop_down_btn[1][1] + drop_down_btn[0][1]) / 2

            max_price_x = (max_price[0][0] + max_price[1][0]) / 2
            max_price_y = (max_price[1][1] + max_price[0][1]) / 2

            max_price_ok_x = (max_price_ok[0][0] + max_price_ok[1][0]) / 2
            max_price_ok_y = (max_price_ok[1][1] + max_price_ok[0][1]) / 2

            return (select_x, select_y), (max_price_x, max_price_y), (max_price_ok_x, max_price_ok_y)
        return None, None, None


class CropListParser(BaseParser):
    def __init__(self, output_path, crop_sales_template, debug=False):
        super().__init__(output_path, debug)
        self.crop_sales_template = cv2.cvtColor(crop_sales_template, cv2.COLOR_RGB2GRAY)

    def parse_image(self, image_rgb, *args, **kwargs):
        print("Manor: %s Look for crops dialog" % datetime.now())
        image_rgb = image_rgb.copy()
        image = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2GRAY)
        match = cv2.matchTemplate(image, self.crop_sales_template, cv2.TM_CCORR_NORMED)
        loc = np.where(match >= 0.89)
        hh, ww = self.crop_sales_template.shape[:2]

        match_points = list(zip(*loc[::-1]))
        if match_points:
            first_match = match_points[0]
            crop_sale = ((first_match[0] + 460, first_match[1] + 245), (first_match[0] + 475, first_match[1] + 260))
            seed_row = ((first_match[0] + 535, first_match[1] + 25), (first_match[0] + 550, first_match[1] + 40))

            if self.debug:
                debug_img = image_rgb.copy()
                self.draw_match_squares(debug_img, match_points, ww, hh)
                cv2.rectangle(debug_img, seed_row[0], seed_row[1], (0, 255, 0), 1)
                cv2.rectangle(debug_img, crop_sale[0], crop_sale[1], (0, 0, 255), 1)
                self.debug_show_im(debug_img, "Crop list")

            seed_x = (seed_row[0][0] + seed_row[1][0]) / 2
            seed_y = (seed_row[1][1] + seed_row[0][1]) / 2
            crop_sell_x = (crop_sale[0][0] + crop_sale[1][0]) / 2
            crop_sell_y = (crop_sale[1][1] + crop_sale[0][1]) / 2
            return (seed_x, seed_y), (crop_sell_x, crop_sell_y)
        return None, None


class ManorDialogParser(BaseParser):
    def __init__(self, output_path, manor_template, debug=False):
        super().__init__(output_path, debug)
        self.manor_template = cv2.cvtColor(manor_template, cv2.COLOR_RGB2GRAY)

    def parse_image(self, image_rgb, *args, **kwargs):
        image_rgb = image_rgb.copy()
        image = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2GRAY)
        match = cv2.matchTemplate(image, self.manor_template, cv2.TM_CCORR_NORMED)
        loc = np.where(match >= 0.89)

        match_points = list(zip(*loc[::-1]))
        if match_points:
            first_points = match_points[0]
            sale_btn = ((first_points[0] + 535, first_points[1] + 275), (first_points[0] + 550, first_points[1] + 290))

            if self.debug:
                debug_img = image_rgb.copy()
                hh, ww = self.manor_template.shape[:2]
                self.draw_match_squares(debug_img, match_points, ww, hh)
                cv2.rectangle(debug_img, sale_btn[0], sale_btn[1], (0, 0, 255), 1)
                self.debug_show_im(debug_img, "Manor dialog")

            sell_x = (sale_btn[0][0] + sale_btn[1][0]) / 2
            sell_y = (sale_btn[1][1] + sale_btn[0][1]) / 2
            return sell_x, sell_y
        return None
