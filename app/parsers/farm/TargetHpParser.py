import cv2
import numpy as np

from app.parsers.BaseParser import BaseParser


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

        # # Square detection
        # for cnt in contours:
        #     approx = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)
        #     if (len(approx) == 4) & (cv2.contourArea(cnt) > 25):  # to discard noise from the color segmentation
        #         contour_poly = cv2.approxPolyDP(cnt, 3, True)
        #         center, radius = cv2.minEnclosingCircle(contour_poly)
        #         color = (0, 255, 0)
        #         cv2.circle(resized, (int(center[0]), int(center[1])), int(radius), color, 2)

        if contours:
            cnt = contours[0]
            approx = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)
            if cv2.contourArea(cnt) > 25:  # to discard noise from the color segmentation
                contour_poly = cv2.approxPolyDP(cnt, 3, True)
                center, radius = cv2.minEnclosingCircle(contour_poly)

                if self.debug:
                    color = (0, 255, 0)
                    cv2.circle(resized, (int(center[0]), int(center[1])), int(radius), color, 2)
                    self.debug_show_im(resized, "ddd")

                resized_width = int(resized.shape[1])
                hp_width = radius * 2

                return int(hp_width * 100 / resized_width)
        else:
            return -1
