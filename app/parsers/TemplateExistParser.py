import numpy as np

from app.parsers.BaseParser import BaseParser
import cv2


class TemplateExistParser(BaseParser):

    def __init__(self, output_path, target_template, debug=False):
        super().__init__(output_path, debug)
        self.target_template = cv2.cvtColor(target_template, cv2.COLOR_RGB2GRAY)

    def parse_image(self, image_rgb, *args, **kwargs):
        return self.is_template_present(image_rgb)

    def is_template_present(self, screen_rgb):
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
