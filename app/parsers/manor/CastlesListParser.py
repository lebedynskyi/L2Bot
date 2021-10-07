import cv2
import numpy as np

from app.parsers.BaseParser import BaseParser


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

            select_btn = ((first_match[0] + 150, first_match[1] + 122), (first_match[0] + 165, first_match[1] + 137))
            max_price_ok = ((first_match[0] + 112, first_match[1] + 187), (first_match[0] + 127, first_match[1] + 202))
            max_price = ((first_match[0] + 210, first_match[1] + 150), (first_match[0] + 230, first_match[1] + 165))

            if self.debug:
                debug_img = image_rgb.copy()
                hh, ww = self.castles_list_template.shape[:2]
                self.draw_match_squares(debug_img, match_points, ww, hh)
                cv2.rectangle(debug_img, select_btn[0], select_btn[1], (0, 0, 255), 1)
                cv2.rectangle(debug_img, max_price_ok[0], max_price_ok[1], (0, 0, 255), 1)
                cv2.rectangle(debug_img, max_price[0], max_price[1], (0, 0, 255), 1)
                self.debug_show_im(debug_img, "Collapsed dialog")

            select_x = (select_btn[0][0] + select_btn[1][0]) / 2
            select_y = (select_btn[1][1] + select_btn[0][1]) / 2

            max_price_x = (max_price[0][0] + max_price[1][0]) / 2
            max_price_y = (max_price[1][1] + max_price[0][1]) / 2

            max_price_ok_x = (max_price_ok[0][0] + max_price_ok[1][0]) / 2
            max_price_ok_y = (max_price_ok[1][1] + max_price_ok[0][1]) / 2

            return (select_x, select_y), (max_price_x, max_price_y), (max_price_ok_x, max_price_ok_y)
        return None, None, None
