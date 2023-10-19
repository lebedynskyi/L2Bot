import logging
import math
from threading import Thread

import cv2
import numpy as np

from app.ocr.recognition import TextRecognition
from app.parser.base import BaseParser

logger = logging.getLogger("NearTargetParser")


class NearTargetParser(BaseParser):
    lower_color = np.array([0, 0, 0])
    upper_color = np.array([0, 0, 0])

    def __init__(self, debug=False):
        super().__init__(debug)
        self.ocr = TextRecognition()

    def parse_image(self, rgb, gray, *args, **kwargs):
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
        title_box = gray[y:y + h, x:x + w]
        player_position = (gray.shape[1] / 2, gray.shape[0] / 2)
        distance = math.dist(player_position, (x, y))

        name = self.ocr.extract(title_box, 3)
        if name is not None and len(name) > 5:
            result.append(NearTargetResult(name, distance))

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

            # just increase the box by 2 pixels around
            result.append([x - 2, y - 2, w + 4, h + 4])

        if self.debug:
            rgb_copy = rgb.copy()
            for [x, y, w, h] in result:
                # draw rectangle around contour on original image
                cv2.rectangle(rgb_copy, (x, y), (x + w, y + h), (0, 0, 255), 1)
            self.show_im(rgb_copy, "Found titles")

        return result


class C3NearTargetsParser(NearTargetParser):
    # Color segmentation
    lower_color = np.array([0, 0, 0])
    upper_color = np.array([179, 9, 255])


class GraciaNearTargetsParser(NearTargetParser):
    # Color segmentation
    lower_color = np.array([0, 0, 0])
    upper_color = np.array([0, 255, 255])


class NearTargetResult:
    def __init__(self, name, distance):
        self.name = name
        self.distance = distance
