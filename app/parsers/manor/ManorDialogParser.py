import cv2
import numpy as np

from app.parsers.BaseParser import BaseParser


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
                self.debug_show_im(debug_img)

            sell_x = (sale_btn[0][0] + sale_btn[1][0]) / 2
            sell_y = (sale_btn[1][1] + sale_btn[0][1]) / 2
            return sell_x, sell_y
        return None
