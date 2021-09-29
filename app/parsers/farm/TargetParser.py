import numpy as np

from app.parsers.Base import BaseParser
import cv2


class TargetParser(BaseParser):

    def __init__(self, output_path, target_template):
        super().__init__(output_path)
        self.target_template = cv2.cvtColor(target_template, cv2.COLOR_RGB2GRAY)

    def parse_image(self, screen_rgb):
        return self.is_target_exist(screen_rgb)

    def is_target_exist(self, screen_rgb):
        image = cv2.cvtColor(screen_rgb, cv2.COLOR_RGB2GRAY)
        match = cv2.matchTemplate(image, self.target_template, cv2.TM_CCORR_NORMED)
        loc = np.where(match >= 0.89)
        match_points = list(zip(*loc[::-1]))
        if match_points:
            if self.debug:
                debug_img = screen_rgb.copy()
                hh, ww = self.target_template.shape[:2]
                self.draw_match_squares(debug_img, match_points, ww, hh)
                self.debug_show_im(debug_img)
            return True
        return False
