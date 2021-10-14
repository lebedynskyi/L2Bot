import cv2
import numpy as np
import pytesseract

from app.parsers.BaseParser import BaseParser


class CastlesListChooserParser(BaseParser):

    def __init__(self, output_path, list_chooser_template, debug=False):
        super().__init__(output_path, debug)
        self.list_chooser_template = cv2.cvtColor(list_chooser_template, cv2.COLOR_RGB2GRAY)

    def parse_image(self, image_rgb, *args, **kwargs):
        looking_castle = kwargs["castle"]

        image_rgb = image_rgb.copy()
        image = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2GRAY)
        match = cv2.matchTemplate(image, self.list_chooser_template, cv2.TM_CCORR_NORMED)

        loc = np.where(match >= 0.89)
        match_points = list(zip(*loc[::-1]))

        castle_x = None
        castle_y = None

        if match_points:
            first_match = match_points[0]

            if self.debug:
                hh, ww = self.list_chooser_template.shape[:2]
                debug_img = image_rgb.copy()
                self.draw_match_squares(debug_img, match_points, ww, hh)
                self.debug_show_im(debug_img, "Castle chooser")

            if looking_castle.castle_number <= 2:
                print("Manor: look for castle {}".format(looking_castle.castle_name))
                for i in range(looking_castle.start_index, looking_castle.finish_index):
                    castle = (
                        # 17 pixels height per 1 castle
                        # (first_match[0] + 116, first_match[1] + 122 + i * 17),
                        # (first_match[0] + 255, first_match[1] + 122 + i * 17 + 17)
                        (first_match[0], first_match[1] + i * 17),
                        (first_match[0] + 140, first_match[1] + i * 17 + 17)
                    )

                    castle_name_string = self._parse_castle_name(image_rgb, castle)
                    if looking_castle.alternative_castle_name is not None and looking_castle.alternative_castle_name in castle_name_string:
                        castle_x = (castle[0][0] + castle[1][0]) / 2
                        castle_y = (castle[1][1] + castle[0][1]) / 2

                    if looking_castle.castle_name in castle_name_string:
                        castle_x = (castle[0][0] + castle[1][0]) / 2
                        castle_y = (castle[1][1] + castle[0][1]) / 2
                        break

            else:
                print("Manor: Use castle position {}".format(looking_castle.castle_number))
                castle = (
                    (first_match[0], first_match[1] + looking_castle.castle_number * 17),
                    (first_match[0] + 140, first_match[1] + looking_castle.castle_number * 17 + 17)
                )
                castle_x = (castle[0][0] + castle[1][0]) / 2
                castle_y = (castle[1][1] + castle[0][1]) / 2

        if castle_y is not None and castle_y is not None:
            return castle_x, castle_y

        print("Manor: Castles not found")
        return None

    def _parse_castle_name(self, screen_rgb, castle_area):
        # dialog_rgb[5:60, 34:300]
        castle_img = screen_rgb[castle_area[0][1]:castle_area[1][1], castle_area[0][0]:castle_area[1][0]]
        gray = cv2.cvtColor(castle_img, cv2.COLOR_RGB2GRAY)
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

        scale_percent = 500  # percent of original size
        width = int(thresh.shape[1] * scale_percent / 100)
        height = int(thresh.shape[0] * scale_percent / 100)
        dim = (width, height)

        # resize image
        resized = cv2.resize(thresh, dim, interpolation=cv2.INTER_AREA)

        blur = cv2.GaussianBlur(resized, (5, 5), 0)
        if self.debug:
            self.debug_show_im(blur, "Debug blurred for text")

        tesseract_config = r"--oem 3 --psm 7 -l eng -c tessedit_char_whitelist= 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'"
        text = pytesseract.image_to_string(blur, lang="eng", config=tesseract_config)
        return text
