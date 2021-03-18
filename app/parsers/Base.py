import os
import cv2

from abc import ABC, abstractmethod


class BaseParser(ABC):
    def __init__(self, output_path, debug=False):
        self.output_path = output_path
        self.debug = debug
        if not os.path.exists(output_path):
            os.makedirs(output_path)

    @abstractmethod
    def parse_image(self, image_rgb):
        raise NotImplementedError("Handler is not implemented")

    def draw_match_squares(self, image, points, width, height):
        for pt in points:
            cv2.rectangle(image, pt, (pt[0] + width, pt[1] + height), (0, 0, 255), 1)

    def debug_show_im(self, img, title="Debug"):
        cv2.imshow(title, img)
        cv2.waitKey(0)
