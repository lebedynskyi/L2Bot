import cv2
import numpy as np

from app.parsers.base import BaseParser


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
            self.write_log("WarnDialog", "Found")
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


class QuizStartDialogParser(BaseParser):
    def __init__(self, output_path, template, debug=False):
        super().__init__(output_path, debug)
        self.template = cv2.cvtColor(template, cv2.COLOR_RGB2GRAY)

    def parse_image(self, image_rgb, *args, **kwargs):
        image_rgb = image_rgb.copy()
        image = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2GRAY)

        header_match = cv2.matchTemplate(image, self.template, cv2.TM_CCORR_NORMED)

        thresh_hold = 0.89
        header_loc = np.where(header_match >= thresh_hold)

        # draw matches
        hh, ww = self.template.shape[:2]
        group_points = list(zip(*header_loc[::-1]))
        if not group_points:
            return None

        self.write_log("QuizStart", "Found")

        dialog_header_pt = group_points[0]

        start_zone = (
            (dialog_header_pt[0] + 130, dialog_header_pt[1] + 80),
            (dialog_header_pt[0] + 160, dialog_header_pt[1] + 60))

        if self.debug:
            debug_img = image_rgb.copy()

            self.draw_match_squares(debug_img, group_points, ww, hh)
            cv2.rectangle(debug_img, start_zone[0], start_zone[1], (0, 0, 255), 1)

            self.debug_show_im(debug_img, "Screenshot")

        return (start_zone[0][0] + start_zone[1][0]) / 2, (start_zone[0][1] + start_zone[1][1]) / 2


class QuizContinueDialogParser(BaseParser):
    def __init__(self, output_path, template, debug=False):
        super().__init__(output_path, debug)
        self.template = cv2.cvtColor(template, cv2.COLOR_RGB2GRAY)

    def parse_image(self, image_rgb, *args, **kwargs):
        image_rgb = image_rgb.copy()
        image = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2GRAY)

        header_match = cv2.matchTemplate(image, self.template, cv2.TM_CCORR_NORMED)

        thresh_hold = 0.89
        header_loc = np.where(header_match >= thresh_hold)

        # draw matches
        hh, ww = self.template.shape[:2]
        group_points = list(zip(*header_loc[::-1]))
        if not group_points:
            return None

        self.write_log("QuizContinue", "Found")

        dialog_header_pt = group_points[0]

        captcha_image_pt = ((dialog_header_pt[0] + 130, dialog_header_pt[1] + 48),
                            (dialog_header_pt[0] + 160, dialog_header_pt[1] + 78))
        look_zone_pt = (
            (dialog_header_pt[0], dialog_header_pt[1] + 90), (dialog_header_pt[0] + ww, dialog_header_pt[1] + 290))

        captcha_img = image_rgb[captcha_image_pt[0][1]:captcha_image_pt[1][1],
                      captcha_image_pt[0][0]:captcha_image_pt[1][0]]

        look_zone_img = image_rgb[look_zone_pt[0][1]:look_zone_pt[1][1],
                        look_zone_pt[0][0]:look_zone_pt[1][0]]

        if self.debug:
            debug_img = image_rgb.copy()

            self.draw_match_squares(debug_img, group_points, ww, hh)
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
            self.draw_match_squares(debug_look_zone_img, target_points, cw, ch)
            self.debug_show_im(debug_look_zone_img, "Target letter in area")

        target_y = int(header_loc[0][0] + 90 + target_loc[0][0])
        target_x = int(header_loc[1][0] + target_loc[1][0])

        if self.debug:
            cv2.rectangle(image_rgb, (target_x, target_y), (target_x + cw, target_y + ch), (0, 0, 255), 1)
            self.debug_show_im(image_rgb, "Target letter on screen")

        return target_x + cw / 2, target_y + ch / 2
