import math
from abc import ABC, abstractmethod
from threading import Thread
from typing import Tuple

import cv2
import numpy as np

from src.ocr.recognition import TextRecognition
from src.parser.result import NearTargetResult, TargetResult, UserStatusResult, ManorWindowResult, ResultSquare, \
    ManorWindowCropListResult, ManorWindowPriceListResult
from src.template import Template


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
                cv2.rectangle(copy, (startX, startY), (end_x, end_y), (255, 255, 255), 2)
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
    def draw_match_squares(image, point: Tuple, height, width, white_color=False):
        color = (0, 0, 255)
        if white_color:
            color = (255, 255, 255)
        cv2.rectangle(image, point, (point[0] + width, point[1] + height), color, 2)


class TemplateExist(BaseParser):
    def __init__(self, template, show_match):
        super().__init__(show_match)
        self.template = template

    def parse(self, rgb, grey, *args, **kwargs):
        return self.match_template(grey, self.template) is not None


class NearTargetsParser(BaseParser, ABC):
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
        # Just increase a box on 4 pixels around
        title_box = gray[y - 4:y + h + 4, x - 4:x + w + 4]
        player_position = (gray.shape[1] / 2, gray.shape[0] / 2)
        distance = math.dist(player_position, (x, y))

        name = self.ocr.extract(title_box, 2, whitelist="ABCDEFGHIJKLMNOPQRSTUVWXVZabcdefghijklmnopqrstuvwxvz ")
        if name is not None and len(name) > 1:
            result.append(NearTargetResult(x, y, w, h, name, distance))

    def _find_title_boxes(self, rgb):

        masked = self.hsv_mask(rgb, self.lower_color, self.upper_color)
        contours, hierarchy = self.find_contours(masked)

        result = []
        for contour in contours:
            # get rectangle bounding contour
            [x, y, w, h] = cv2.boundingRect(contour)

            # Don't plot small and big false positives that aren't text
            if w < 10 or h < 10 or h > 50:
                continue

            # so if title has 2 - 3 words. we need to find same boxes on the same y coordinate and join it.
            is_merged = False
            for idx in range(len(result)):
                already_added = result[idx]
                added_center_line = already_added[1] + int(already_added[3] / 2)
                current_center_line = y + int(h / 2)
                if already_added[1] == y or abs(added_center_line - current_center_line) <= 2:
                    extended = union(already_added, [x, y, w, h])
                    result[idx] = extended
                    is_merged = True

            if not is_merged:
                result.append([x, y, w, h])

        if self.debug:
            rgb_copy = rgb.copy()
            for [x, y, w, h] in result:
                # draw rectangle around contour
                cv2.rectangle(rgb_copy, (x, y), (x + w, y + h), (0, 0, 255), 1)
            self.show_im(rgb_copy, "Found mobs titles")

        return result


class TargetParser(BaseParser, ABC):
    x_offset = 0
    y_offset = 0
    w = 0
    h = 0
    lower_color = np.array([0, 0, 0])
    upper_color = np.array([0, 0, 0])

    def __init__(self, templates: Template, debug=False):
        super().__init__(debug)
        self.templates = templates

    def parse(self, rgb, gray, *args, **kwargs):
        result = TargetResult()
        target_match = self.match_template(gray, self.templates.ui_target)
        if target_match is not None:
            result.exist = True
            result.hp = self._parse_hp(rgb, target_match)
        return result

    def _parse_hp(self, rgb, match):
        cropped = rgb[match[1] + self.y_offset:match[1] + self.y_offset + self.h,
                  match[0] + self.x_offset:match[0] + self.x_offset + self.w]
        if self.debug:
            self.show_im(cropped, "Target HP area")

        width = int(cropped.shape[1] * 3)
        height = int(cropped.shape[0] * 3)
        dim = (width, height)

        # resize image
        resized = cv2.resize(cropped, dim, interpolation=cv2.INTER_AREA)
        if self.debug:
            self.show_im(resized, "Resized target hp target")

        masked = self.hsv_mask(resized, self.lower_color, self.upper_color)
        contours, hierarchy = self.find_contours(masked)

        if contours:
            cnt = contours[0]
            approx = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)
            if cv2.contourArea(cnt) > 10:  # to discard noise from the color segmentation
                contour_poly = cv2.approxPolyDP(cnt, 3, True)
                center, radius = cv2.minEnclosingCircle(contour_poly)

                if self.debug:
                    color = (0, 255, 0)
                    cv2.circle(resized, (int(center[0]), int(center[1])), int(radius), color, 2)
                    self.show_im(resized, "Found limits")

                resized_width = int(resized.shape[1])
                hp_width = radius * 2

                return int(hp_width * 100 / resized_width)

        return 0


class UserStatusParser(BaseParser, ABC):
    hp_x_offset = 0
    hp_y_offset = 0
    hp_h = 0
    hp_w = 0

    mp_x_offset = 0
    mp_y_offset = 0
    mp_h = 0
    mp_w = 0

    cp_x_offset = 0
    cp_y_offset = 0
    cp_h = 0
    cp_w = 0

    lower_color = np.array([0, 0, 0])
    upper_color = np.array([0, 0, 0])

    def __init__(self, templates: Template, debug=False):
        super().__init__(debug)
        self.templates = templates
        self.ocr = TextRecognition(debug=debug)

    def parse(self, rgb, gray, *args, **kwargs):
        result = UserStatusResult()
        status_match = self.match_template(gray, self.templates.user_status)
        if status_match is not None:
            masked = self.hsv_mask(rgb, self.lower_color, self.upper_color)
            if self.debug:
                self.show_im(masked, "Masked image")

            grey_scaled = cv2.cvtColor(masked, cv2.COLOR_RGB2GRAY)

            # result.cp = self._parse_cp(grey_scaled, status_match)
            result.hp = self._parse_hp(grey_scaled, status_match)
            # result.mp = self._parse_mp(grey_scaled, status_match)
        return result

    def _parse_hp(self, grey, match):
        cropped = grey[match[1] + self.hp_y_offset:match[1] + self.hp_y_offset + self.hp_h,
                  match[0] + self.hp_x_offset:match[0] + self.hp_x_offset + self.hp_w]

        if self.debug:
            self.show_im(cropped, "Status HP area")

        try:
            hp = self.ocr.extract(cropped, 3, whitelist="0123456789/")
            split = hp.split("/")
            return self._cleanup_values(int(split[0]), int(split[1]))
        except:
            pass
        return None

    def _cleanup_values(self, cur, max):
        s_cur = str(cur)
        s_max = str(cur)
        if len(s_cur) > len(s_max) or cur > max:
            return int(s_cur[1:]), max

        return cur, max

    def _parse_mp(self, grey, match):
        cropped = grey[match[1] + self.mp_y_offset:match[1] + self.mp_y_offset + self.mp_h,
                  match[0] + self.mp_x_offset:match[0] + self.mp_x_offset + self.mp_w]

        if self.debug:
            self.show_im(cropped, "Status MP area")

        try:
            mp = self.ocr.extract(cropped, 2)
            split = mp.split("/")
            return int(split[0]), int(split[1])
        except:
            pass
        return None

    def _parse_cp(self, grey, match):
        cropped = grey[match[1] + self.cp_y_offset:match[1] + self.cp_y_offset + self.cp_h,
                  match[0] + self.cp_x_offset:match[0] + self.cp_x_offset + self.cp_w]

        if self.debug:
            self.show_im(cropped, "Status CP area")

        try:
            cp = self.ocr.extract(cropped, 2)
            split = cp.split("/")
            return int(split[0]), int(split[1])
        except:
            pass
        return None


class ManorParser(BaseParser):
    window_sell_btn_x_offset = 0
    window_sell_btn_y_offset = 0
    windows_sell_btn_h = 0
    windows_sell_btn_w = 0

    list_sell_btn_x_offset = 0
    list_sell_btn_y_offset = 0
    list_sell_btn_h = 0
    list_sell_btn_w = 0

    list_crop_item_x_offset = 0
    list_crop_item_y_offset = 0
    list_crop_item_h = 16
    list_crop_item_w = 300

    price_crop_item_x_offset = 0
    price_crop_item_y_offset = 0
    price_crop_item_h = 16
    price_crop_item_w = 80

    price_chooser_x_offset = 0
    price_chooser_y_offset = 0
    price_chooser_h = 0
    price_chooser_w = 0

    price_max_x_offset = 0
    price_max_y_offset = 0
    price_max_h = 0
    price_max_w = 0

    price_ok_x_offset = 0
    price_ok_y_offset = 0
    price_ok_h = 0
    price_ok_w = 0

    def __init__(self, templates: Template, debug=False):
        super().__init__(debug)
        self.templates = templates

    def parse(self, rgb, gray, *args, **kwargs):
        pass

    def manor_window(self, grey):
        result = ManorWindowResult()
        target_match = self.match_template(grey, self.templates.manor_window)

        if target_match is not None:
            sell_btn = ResultSquare(
                x=target_match[0] + self.window_sell_btn_x_offset,
                y=target_match[1] + self.window_sell_btn_y_offset,
                h=self.windows_sell_btn_h,
                w=self.windows_sell_btn_w
            )
            result.exist = True
            result.sell_crop_btn = sell_btn

            if self.debug:
                self.draw_match_squares(grey, (sell_btn.x, sell_btn.y), sell_btn.h, sell_btn.w, white_color=True)
                self.show_im(grey, "Manor window sell crop BTN", )

        return result

    # returns position (int, int) of sell button in crop sale window
    def crop_list(self, grey):
        result = ManorWindowCropListResult()
        target_match = self.match_template(grey, self.templates.manor_crop_list)

        if target_match is not None:
            sell_btn = ResultSquare(
                x=target_match[0] + self.list_sell_btn_x_offset,
                y=target_match[1] + self.list_sell_btn_y_offset,
                h=self.list_sell_btn_h,
                w=self.list_sell_btn_w
            )
            first_crop_item = ResultSquare(
                x=target_match[0] + self.list_crop_item_x_offset,
                y=target_match[1] + self.list_crop_item_y_offset,
                h=self.list_crop_item_h,
                w=self.list_crop_item_w
            )

            second_crop_item = ResultSquare(
                x=target_match[0] + self.list_crop_item_x_offset,
                y=target_match[1] + self.list_crop_item_y_offset + self.list_crop_item_h,
                h=self.list_crop_item_h,
                w=self.list_crop_item_w
            )

            result.exist = True
            result.sell_crop_btn = sell_btn
            result.first_crop_item = first_crop_item
            result.second_crop_item = second_crop_item

            if self.debug:
                self.draw_match_squares(grey, (sell_btn.x, sell_btn.y), sell_btn.h, sell_btn.w, white_color=True)
                self.draw_match_squares(grey, (first_crop_item.x, first_crop_item.y), first_crop_item.h, first_crop_item.w, white_color=True)
                self.draw_match_squares(grey, (second_crop_item.x, second_crop_item.y), second_crop_item.h, second_crop_item.w, white_color=True)
                self.show_im(grey, "Manor crop list", )

        return result

    def price_list(self, grey):
        result = ManorWindowPriceListResult()
        target_match = self.match_template(grey, self.templates.manor_price_list)
        if target_match is not None:
            result.exist = True

        ok_btn = ResultSquare(
            x=target_match[0] + self.price_ok_x_offset,
            y=target_match[1] + self.price_ok_y_offset,
            h=self.price_ok_h,
            w=self.price_ok_w
        )

        max_price_btn = ResultSquare(
            x=target_match[0] + self.price_max_x_offset,
            y=target_match[1] + self.price_max_y_offset,
            h=self.price_max_h,
            w=self.price_max_w
        )

        chooser_btn = ResultSquare(
            x=target_match[0] + self.price_chooser_x_offset,
            y=target_match[1] + self.price_chooser_y_offset,
            h=self.price_chooser_h,
            w=self.price_chooser_w
        )

        first_crop_item = ResultSquare(
            x=chooser_btn.x + self.price_crop_item_x_offset,
            y=chooser_btn.y + self.price_crop_item_y_offset,
            h=self.price_crop_item_h,
            w=self.price_crop_item_w
        )

        second_crop_item = ResultSquare(
            x=chooser_btn.x + self.price_crop_item_x_offset,
            y=chooser_btn.y + self.price_crop_item_y_offset + self.price_crop_item_h,
            h=self.price_crop_item_h,
            w=self.price_crop_item_w
        )

        third_crop_item = ResultSquare(
            x=chooser_btn.x + self.price_crop_item_x_offset,
            y=chooser_btn.y + self.price_crop_item_y_offset + self.price_crop_item_h * 2,
            h=self.price_crop_item_h,
            w=self.price_crop_item_w
        )

        fourth_crop_item = ResultSquare(
            x=chooser_btn.x + self.price_crop_item_x_offset,
            y=chooser_btn.y + self.price_crop_item_y_offset + self.price_crop_item_h * 3,
            h=self.price_crop_item_h,
            w=self.price_crop_item_w
        )

        result.ok_btn = ok_btn
        result.max_price_btn = max_price_btn
        result.chooser_btn = chooser_btn
        result.first_crop_item = first_crop_item
        result.second_crop_item = second_crop_item
        result.third_crop_item = third_crop_item
        result.fourth_crop_item = fourth_crop_item

        if self.debug:
            self.draw_match_squares(grey, (ok_btn.x, ok_btn.y), ok_btn.h, ok_btn.w, white_color=True)
            self.draw_match_squares(grey, (max_price_btn.x, max_price_btn.y), max_price_btn.h, max_price_btn.w,white_color=True)
            self.draw_match_squares(grey, (chooser_btn.x, chooser_btn.y), chooser_btn.h,chooser_btn.w, white_color=True)

            self.draw_match_squares(grey, (first_crop_item.x, first_crop_item.y), first_crop_item.h,first_crop_item.w, white_color=True)
            self.draw_match_squares(grey, (second_crop_item.x, second_crop_item.y), second_crop_item.h,second_crop_item.w, white_color=True)
            self.draw_match_squares(grey, (third_crop_item.x, third_crop_item.y), third_crop_item.h,third_crop_item.w, white_color=True)
            self.draw_match_squares(grey, (fourth_crop_item.x, fourth_crop_item.y), fourth_crop_item.h,fourth_crop_item.w, white_color=True)
            self.show_im(grey, "Manor chooser list", )

        return result

    def price_list_chooser(self, grey):
        raise NotImplementedError("Not implemented")

def union(a, b):
    x = min(a[0], b[0])
    y = min(a[1], b[1])
    w = max(a[0] + a[2], b[0] + b[2]) - x
    h = max(a[1] + a[3], b[1] + b[3]) - y
    return x, y, w, h
