import cv2
import numpy as np

from app.parsers.base import BaseParser


class TargetHpParser(BaseParser):
    def parse_image(self, image_rgb, *args, **kwargs):
        cropped_hp_area = self.crop_hp_area(image_rgb)
        return self.parse_hp(cropped_hp_area)

    def crop_hp_area(self, image_rgb):
        return image_rgb[26:30, 7:157]

    def parse_hp(self, hp_area):
        hp_area = cv2.cvtColor(hp_area, cv2.COLOR_BGR2RGB)

        width = int(hp_area.shape[1] * 5)
        height = int(hp_area.shape[0] * 5)
        dim = (width, height)

        # resize image
        resized = cv2.resize(hp_area, dim, interpolation=cv2.INTER_AREA)
        if self.debug:
            self.debug_show_im(resized, "Resized target")

        # Color segmentation
        hsv = cv2.cvtColor(resized, cv2.COLOR_BGR2HSV)
        lower_red = np.array([0, 50, 50])
        upper_red = np.array([5, 255, 255])
        mask = cv2.inRange(hsv, lower_red, upper_red)
        res = cv2.bitwise_and(resized, resized, mask=mask)

        # Contour exctraction
        imgray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(imgray, (5, 5), 0)
        ret, thresholded = cv2.threshold(blurred, 50, 255, 0)
        contours, h = cv2.findContours(thresholded, 1, 2)

        if contours:
            cnt = contours[0]
            approx = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)
            if cv2.contourArea(cnt) > 25:  # to discard noise from the color segmentation
                contour_poly = cv2.approxPolyDP(cnt, 3, True)
                center, radius = cv2.minEnclosingCircle(contour_poly)

                if self.debug:
                    color = (0, 255, 0)
                    cv2.circle(resized, (int(center[0]), int(center[1])), int(radius), color, 2)
                    self.debug_show_im(resized, "Found limits")

                resized_width = int(resized.shape[1])
                hp_width = radius * 2

                return int(hp_width * 100 / resized_width)
        else:
            return -1


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
