import numpy as np

from app.parsers.BaseParser import BaseParser
import cv2


class TargetWindowParser(BaseParser):

    def __init__(self, output_path, target_template, debug=False):
        super().__init__(output_path, debug)
        self.target_template = cv2.cvtColor(target_template, cv2.COLOR_RGB2GRAY)

    def parse_image(self, image_rgb, *args, **kwargs):
        return self.extract_target_window(image_rgb)

    def extract_target_window(self, image_rgb):
        image = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2GRAY)
        match = cv2.matchTemplate(image, self.target_template, cv2.TM_CCORR_NORMED)
        loc = np.where(match >= 0.89)
        match_points = list(zip(*loc[::-1]))
        if match_points:
            if self.debug:
                debug_img = image_rgb.copy()
                hh, ww = self.target_template.shape[:2]
                self.draw_match_squares(debug_img, match_points, ww, hh)
                self.debug_show_im(debug_img)
            return self.crop_target_window(image_rgb, match_points)
        return None

    def crop_target_window(self, image, target_points):
        pt = target_points[0]
        crop_dialog = image[pt[1]:pt[1] + 74, pt[0] + 10:pt[0] + 174]
        if self.debug:
            self.debug_show_im(crop_dialog, "Debug cropped target")
        return crop_dialog
