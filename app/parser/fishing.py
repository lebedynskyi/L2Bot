import cv2
import numpy as np

from app.ocr.recognition import NumbersRecognition
from app.parser.base import BaseParser
from app.template import GraciaTemplates


class FishingResult:
    is_fishing = False
    seconds_left = None
    hp_percent = None


class GraciaFishing(BaseParser):
    def __init__(self, templates: GraciaTemplates, debug=False):
        super().__init__(debug)
        self.templates = templates
        self.ocr = NumbersRecognition()

    def parse_image(self, rgb, grey, *args, **kwargs):
        result = FishingResult()

        fishing_match = self.match_template(grey, self.templates.ui_fishing_dialog)
        if fishing_match:
            result.is_fishing = True
            result.hp_percent = self._parse_hp(fishing_match, rgb, grey)
            result.seconds_left = self._parse_second(fishing_match, rgb, grey)

        return result

    def _parse_hp(self, fishing_match, rgb, grey):
        start_x, start_y = fishing_match[0] + 24, fishing_match[1] + 251
        end_x, end_y = start_x + 228, start_y + 15
        hp_img_rgb = rgb[start_y:end_y, start_x:end_x]
        if self.debug:
            self.show_im(hp_img_rgb)
        hp = self._extract_fish_hp(hp_img_rgb)
        return hp

    def _parse_second(self, fishing_match, rgb, grey):
        start_x, start_y = fishing_match[0] + 130, fishing_match[1] + 225
        end_x, end_y = start_x + 45, start_y + 25
        seconds_img = grey[start_y:end_y, start_x:end_x]
        # if self.show_match:
        #     self.show_im(seconds_img)

        return self.ocr.extract(seconds_img, 2)

    def _extract_fish_hp(self, hp_area_rgb):
        width = int(hp_area_rgb.shape[1] * 2)
        height = int(hp_area_rgb.shape[0] * 2)
        dim = (width, height)

        # resize image
        resized = cv2.resize(hp_area_rgb, dim, interpolation=cv2.INTER_AREA)
        if self.debug:
            self.show_im(resized, "Resized fish hp target")

        # Color segmentation
        lower_color = np.array([88, 107, 115])
        upper_color = np.array([179, 255, 255])
        masked = self.hsv_mask(resized, lower_color, upper_color)

        # Contour exctraction
        contours, h = self.find_contours(masked)

        if contours:
            cnt = contours[0]
            approx = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)
            if cv2.contourArea(cnt) > 25:  # to discard noise from the color segmentation
                contour_poly = cv2.approxPolyDP(cnt, 3, True)
                center, radius = cv2.minEnclosingCircle(contour_poly)

                if self.debug:
                    color = (0, 255, 0)
                    cv2.circle(resized, (int(center[0]), int(center[1])), int(radius), color, 2)
                    self.show_im(resized, "Found limits")

                resized_width = int(resized.shape[1])
                hp_width = radius * 2

                return int(hp_width * 100 / resized_width)

        return None
