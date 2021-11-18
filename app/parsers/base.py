from datetime import datetime
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
    def parse_image(self, image_rgb, *args, **kwargs):
        raise NotImplementedError("Handler is not implemented")

    def draw_match_squares(self, image, points, width, height):
        for pt in points:
            cv2.rectangle(image, pt, (pt[0] + width, pt[1] + height), (0, 0, 255), 1)

    def debug_show_im(self, img, title="Debug"):
        cv2.imshow(title, img)
        cv2.setWindowProperty(title, cv2.WND_PROP_VISIBLE, 1)
        cv2.waitKey(0)

    def debug_write_im(self, img):
        cv2.imwrite("res/output/temp.png", img)

    def write_log(self, tag, msg):
        time = datetime.now()
        print("|{0}|  {1}: {2}".format(time, tag, msg))
