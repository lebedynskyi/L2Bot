import numpy as np
from PIL import ImageGrab


class UserStatusLogic:
    def __init__(self, status_parser, player):
        self.status_parser = status_parser
        self.player = player

    def check_user_status(self):
        screenshot = ImageGrab.grab()
        screenshot_image = np.array(screenshot)
        hp_coef = self.status_parser.parse_image(screenshot_image)

        if hp_coef <= 0.4:
            print("StatusParser: player HP coef -> " % hp_coef)
            self.player.play_warning()

        return 1