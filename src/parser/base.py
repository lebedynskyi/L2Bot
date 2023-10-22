import math
from abc import ABC, abstractmethod
from threading import Thread

import cv2
import numpy as np

from src.ocr.recognition import TextRecognition
from src.parser.result import NearTargetResult, TargetResult


class BaseParser(ABC):
    def __init__(self, debug=False):
        self.debug = debug

    @abstractmethod
    def parse(self, rgb, gray, *args, **kwargs):
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


class TemplateExist(BaseParser):
    def __init__(self, template, show_match):
        super().__init__(show_match)
        self.template = template

    def parse_image(self, rgb, grey, *args, **kwargs):
        return self.match_template(grey, self.template) is not None


class NearTargetParser(BaseParser):
    lower_color = np.array([0, 0, 0])
    upper_color = np.array([0, 0, 0])

    def __init__(self, debug=False):
        super().__init__(debug)
        self.ocr = TextRecognition()

    def parse(self, rgb, gray, *args, **kwargs):
        title_boxes = self._find_title_boxes(rgb)
        threads = []
        result = []

        for box in title_boxes:
            t = Thread(target=self._parse_title_thread, args=[gray, box, result], daemon=False)
            t.start()
            threads.append(t)

        for x in threads:
            x.join()

        return sorted(result, key=lambda r: r.distance)

    def _parse_title_thread(self, gray, box_data, result):
        [x, y, w, h] = box_data
        # Just increase a box on 2 pixels around
        title_box = gray[y - 2:y + h + 2, x - 2:x + w + 2]
        player_position = (gray.shape[1] / 2, gray.shape[0] / 2)
        distance = math.dist(player_position, (x, y))

        name = self.ocr.extract(title_box, 2)
        if name is not None and len(name) > 1:
            result.append(NearTargetResult(x, y, w, h, name, distance))

    def _find_title_boxes(self, rgb):

        masked = self.hsv_mask(rgb, self.lower_color, self.upper_color)
        contours, hierarchy = self.find_contours(masked)

        result = []

        for contour in contours:
            # get rectangle bounding contour
            [x, y, w, h] = cv2.boundingRect(contour)

            # Don't plot small false positives that aren't text
            if (w < 20 or h < 10) or h > 20:
                continue

            # so if title has 2 words. we need to find same boxes on the same y coordinate and join it.
            is_merged = False
            for idx in range(len(result)):
                already_added = result[idx]

                if already_added[1] == y:
                    extended = union(already_added, [x, y, w, h])
                    result[idx] = extended
                    is_merged = True
                    break

            # just increase the box by 2 pixels around
            if not is_merged:
                result.append([x, y, w, h])

        if self.debug:
            rgb_copy = rgb.copy()
            for [x, y, w, h] in result:
                # draw rectangle around contour
                cv2.rectangle(rgb_copy, (x, y), (x + w, y + h), (0, 0, 255), 1)
            self.show_im(rgb_copy, "Found mobs titles")

        return result


class TargetParser(BaseParser):
    x_offset = 0
    y_offset = 0
    w = 0
    h = 0
    lower_color = np.array([0, 0, 0])
    upper_color = np.array([0, 0, 0])

    def __init__(self, template, debug=False):
        super().__init__(debug)
        self.template = template

    def parse(self, rgb, gray, *args, **kwargs):
        result = TargetResult()
        found_target = self.match_template(gray, self.template)
        print("ddd")


def union(a, b):
    x = min(a[0], b[0])
    y = min(a[1], b[1])
    w = max(a[0] + a[2], b[0] + b[2]) - x
    h = max(a[1] + a[3], b[1] + b[3]) - y
    return (x, y, w, h)
