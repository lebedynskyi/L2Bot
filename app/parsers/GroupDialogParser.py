import cv2
import numpy as np

from app.parsers.Base import BaseParser


# Todo decompose for different methods
class GroupDialogParser(BaseParser):
    def __init__(self, output_path, template, debug=False):
        super().__init__(output_path, debug)
        self.template = cv2.cvtColor(template, cv2.COLOR_RGB2GRAY)

    def parse_image(self, screen_rgb):
        image_rgb = screen_rgb.copy()
        image = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2GRAY)

        header_match = cv2.matchTemplate(image, self.template, cv2.TM_CCORR_NORMED)

        thresh_hold = 0.89
        header_loc = np.where(header_match >= thresh_hold)

        # draw matches
        hh, ww = self.template.shape[:2]
        warning_points = list(zip(*header_loc[::-1]))
        if not warning_points:
            return None

        print("WarnDialog: Group found")

        dialog_header_pt = warning_points[0]

        captcha_image_pt = ((dialog_header_pt[0] + 225, dialog_header_pt[1] + 80),
                            (dialog_header_pt[0] + 256, dialog_header_pt[1] + 112))
        look_zone_pt = (
            (dialog_header_pt[0], dialog_header_pt[1] + 125), (dialog_header_pt[0] + ww, dialog_header_pt[1] + 206))

        captcha_img = image_rgb[captcha_image_pt[0][1]:captcha_image_pt[1][1],
                      captcha_image_pt[0][0]:captcha_image_pt[1][0]]

        look_zone_img = image_rgb[look_zone_pt[0][1]:look_zone_pt[1][1],
                        look_zone_pt[0][0]:look_zone_pt[1][0]]

        if self.debug:
            debug_img = image_rgb.copy()

            self.draw_square(debug_img, warning_points, ww, hh)
            cv2.rectangle(debug_img, captcha_image_pt[0], captcha_image_pt[1], (0, 0, 255), 1)
            cv2.rectangle(debug_img, look_zone_pt[0], look_zone_pt[1], (0, 0, 255), 1)

            self.debug_show_im(debug_img, "Screenshot")
            self.debug_show_im(captcha_img, "Look letter")
            self.debug_show_im(look_zone_img, "Look area")

        look_zone_img_g = cv2.cvtColor(look_zone_img, cv2.COLOR_RGB2GRAY)
        captcha_img_g = cv2.cvtColor(captcha_img, cv2.COLOR_RGB2GRAY)

        target_match = cv2.matchTemplate(look_zone_img_g, captcha_img_g, cv2.TM_CCORR_NORMED)
        target_loc = np.where(target_match >= thresh_hold)
        target_points = list(zip(*target_loc[::-1]))

        ch, cw = captcha_img.shape[:2]
        if self.debug:
            debug_look_zone_img = look_zone_img.copy()
            self.draw_square(debug_look_zone_img, target_points, cw, ch)
            self.debug_show_im(debug_look_zone_img, "Target letter")

        target_y = int(header_loc[0][0] + 125 + target_loc[0])
        target_x = int(header_loc[1][0] + target_loc[1])

        if self.debug:
            cv2.rectangle(screen_rgb, (target_x, target_y), (target_x + cw, target_y + ch), (0, 0, 255), 1)
            self.debug_show_im(screen_rgb, "Target letter on screen")

        return target_x + cw / 2, target_y + ch / 2
