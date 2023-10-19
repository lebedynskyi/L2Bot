from abc import ABC, abstractmethod

import cv2
import numpy as np


class BaseParser(ABC):
    def __init__(self, debug=False):
        self.debug = debug

    @abstractmethod
    def parse_image(self, rgb, gray, *args, **kwargs):
        raise NotImplementedError("Handler is not implemented")

    def match_template(self, source_grey, target_grey):
        match = cv2.matchTemplate(source_grey, target_grey, cv2.TM_CCOEFF_NORMED)

        loc = np.where(match >= 0.89)
        match_points = list(zip(*loc[::-1]))

        if match_points:
            if self.debug:
                copy = source_grey.copy()
                title = self.__class__.__name__

                (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(match)
                (startX, startY) = maxLoc
                end_x = startX + target_grey.shape[1]
                end_y = startY + target_grey.shape[0]
                cv2.rectangle(copy, (startX, startY), (end_x, end_y), (255, 255, 255), 3)
                cv2.imshow(title, copy)
                cv2.waitKey(0)

            return match_points[0]

        return None

    @staticmethod
    def hsv_mask(image_rgb, lower_color, upper_color):
        hsv = cv2.cvtColor(image_rgb, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower_color, upper_color)
        return cv2.bitwise_and(image_rgb, image_rgb, mask=mask)

    @staticmethod
    def find_contours(masked):
        img_gray = cv2.cvtColor(masked, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(img_gray, (5, 5), 0)
        ret, threshold = cv2.threshold(blurred, 50, 255, 0)
        return cv2.findContours(threshold, 1, 2)

    def show_im(self, img, title=None):
        copy = img.copy()

        if title is None:
            title = self.__class__.__name__

        cv2.imshow(title, copy)
        cv2.setWindowProperty(title, cv2.WND_PROP_VISIBLE, 1)
        cv2.waitKey(0)

    @staticmethod
    def draw_match_squares(image, points, width, height):
        for pt in points:
            cv2.rectangle(image, pt, (pt[0] + width, pt[1] + height), (0, 0, 255), 1)
