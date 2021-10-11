from app.parsers.BaseParser import BaseParser

import cv2
import numpy as np


class WarnDialogParser(BaseParser):
    def __init__(self, env_path, warning_template, debug=False):
        super().__init__(env_path, debug)
        self.template = cv2.cvtColor(warning_template, cv2.COLOR_RGB2GRAY)

    def parse_image(self, image_rgb, *args, **kwargs):
        image_rgb = image_rgb.copy()
        image = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2GRAY)

        match = cv2.matchTemplate(image, self.template, cv2.TM_CCORR_NORMED)

        thresh_hold = 0.89
        loc = np.where(match >= thresh_hold)

        # draw matches
        hh, ww = self.template.shape[:2]
        warning_points = list(zip(*loc[::-1]))
        if warning_points:
            warn_pt = warning_points[0]
            ok_square = ((warn_pt[0] + 92, warn_pt[1] + 92), (warn_pt[0] + 112, warn_pt[1] + 112))
            cancel_square = ((warn_pt[0] + 175, warn_pt[1] + 92), (warn_pt[0] + 195, warn_pt[1] + 112))
            if self.debug:
                debug_img = image_rgb.copy()

                self.draw_match_squares(debug_img, warning_points, ww, hh)
                cv2.rectangle(debug_img, ok_square[0], ok_square[1], (0, 0, 255), 1)
                cv2.rectangle(debug_img, cancel_square[0], cancel_square[1], (0, 0, 255), 1)

                self.debug_show_im(debug_img)

            ok_x = (ok_square[0][0] + ok_square[1][0]) / 2
            ok_y = (ok_square[1][1] + ok_square[0][1]) / 2

            cancel_x = (cancel_square[0][0] + cancel_square[1][0]) / 2
            cancel_y = (cancel_square[1][1] + cancel_square[0][1]) / 2
            return self.crop_dialog(image_rgb, warning_points), (ok_x, ok_y), (cancel_x, cancel_y)
        return None, None, None

    def crop_dialog(self, image, warn_points):
        pt = warn_points[0]
        crop_dialog = image[pt[1] - 7:pt[1] + 120, pt[0] - 10:pt[0] + 294]
        if self.debug:
            self.debug_show_im(crop_dialog, "Debug cropped dialog")
        return crop_dialog
