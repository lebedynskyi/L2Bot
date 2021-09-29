from datetime import datetime

import numpy as np

from app.parsers.Base import BaseParser
import cv2


class TargetParser(BaseParser):

    def __init__(self, output_path, target_template):
        super().__init__(output_path)

        self.target_template = target_template

    def parse_image(self, screen_rgb):
        return self.is_target_exist(screen_rgb)

    def is_target_exist(self, screen_rgb):
        print("Manor: %s Look for Manor dialog" % datetime.now())
        image_rgb = screen_rgb.copy()
        image = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2GRAY)
        match = cv2.matchTemplate(image, self.target_template, cv2.TM_CCORR_NORMED)
        if match:
            if self.debug:
                debug_img = screen_rgb.copy()
                loc = np.where(match >= 0.89)
                match_points = list(zip(*loc[::-1]))
                hh, ww = self.target_template.shape[:2]
                self.draw_match_squares(debug_img, match_points, ww, hh)
                self.debug_show_im(debug_img)

        return match is not None
