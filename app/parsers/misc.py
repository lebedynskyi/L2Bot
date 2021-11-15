import cv2
import numpy as np

from app.parsers.base import BaseParser


class ColorParser(BaseParser):
    def __init__(self, output_path, area_size, debug=False):
        super().__init__(output_path, debug)
        self.area_size = area_size

    def parse_image(self, image_rgb, *args, **kwargs):
        points = kwargs["points"]
        if self.debug:
            debug_img = image_rgb.copy()
            for p in points:
                cv2.rectangle(img=debug_img, pt1=p, pt2=(p[0] + self.area_size, p[1] + self.area_size),
                              color=(0, 0, 255), thickness=2)

            self.debug_show_im(debug_img, "Interested areas")

        colors = []
        for p in points:
            area = self.crop_area(image_rgb, p)
            avg_color_per_row = np.average(area, axis=0)
            avg_color = np.average(avg_color_per_row, axis=0)
            colors.append(avg_color)

        return colors

    def crop_area(self, image, point):
        return image[point[1]:point[1] + self.area_size, point[0]:point[0] + self.area_size]


class TemplateExistParser(BaseParser):

    def __init__(self, output_path, target_template, debug=False):
        super().__init__(output_path, debug)
        self.target_template = cv2.cvtColor(target_template, cv2.COLOR_RGB2GRAY)

    def parse_image(self, image_rgb, *args, **kwargs):
        return self.is_template_present(image_rgb)

    def is_template_present(self, screen_rgb):
        image = cv2.cvtColor(screen_rgb, cv2.COLOR_RGB2GRAY)
        match = cv2.matchTemplate(image, self.target_template, cv2.TM_CCORR_NORMED)
        loc = np.where(match >= 0.89)
        match_points = list(zip(*loc[::-1]))
        if match_points:
            if self.debug:
                debug_img = screen_rgb.copy()
                hh, ww = self.target_template.shape[:2]
                self.draw_match_squares(debug_img, match_points, ww, hh)
                self.debug_show_im(debug_img)
            return True
        return False
