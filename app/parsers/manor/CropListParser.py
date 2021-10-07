from datetime import datetime

import cv2
import numpy as np

from app.parsers.BaseParser import BaseParser


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
            crop_sale = ((first_match[0] + 470, first_match[1] + 5), (first_match[0] + 485, first_match[1] + 20))
            seed_row = ((first_match[0] + 50, first_match[1] - 187), (first_match[0] + 65, first_match[1] - 202))

            if self.debug:
                debug_img = image_rgb.copy()
                self.draw_match_squares(debug_img, match_points, ww, hh)
                cv2.rectangle(debug_img, seed_row[0], seed_row[1], (0, 0, 255), 1)
                cv2.rectangle(debug_img, crop_sale[0], crop_sale[1], (0, 0, 255), 1)
                self.debug_show_im(debug_img)

            seed_x = (seed_row[0][0] + seed_row[1][0]) / 2
            seed_y = (seed_row[1][1] + seed_row[0][1]) / 2
            crop_sell_x = (crop_sale[0][0] + crop_sale[1][0]) / 2
            crop_sell_y = (crop_sale[1][1] + crop_sale[0][1]) / 2
            return (seed_x, seed_y), (crop_sell_x, crop_sell_y)
        return None, None
