import cv2
import numpy as np

from app.parsers.Base import BaseParser


class UserDeathStatusParser(BaseParser):
    def __init__(self, env_path, death_template, debug=False):
        super().__init__(env_path, debug)
        self.template = cv2.cvtColor(death_template, cv2.COLOR_RGB2GRAY)

    def parse_image(self, screen_rgb):
        return self.find_death_dialog(screen_rgb)

    def find_death_dialog(self, screen_rgb):
        image_rgb = screen_rgb.copy()
        image = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2GRAY)

        match = cv2.matchTemplate(image, self.template, cv2.TM_CCORR_NORMED)

        thresh_hold = 0.89
        loc = np.where(match >= thresh_hold)

        # draw matches
        hh, ww = self.template.shape[:2]
        match_points = list(zip(*loc[::-1]))

        if match_points and self.debug:
            debug_img = image_rgb.copy()
            self.draw_match_squares(debug_img, match_points, ww, hh)
            self.debug_show_im(debug_img, "Death dialog")

        return len(match_points) > 0
