import numpy as np
from PIL import ImageGrab


class UserDeathLogic:
    def __init__(self, death_parser, player):
        self.death_parser = death_parser
        self.player = player

    def check_is_dead(self):
        screenshot = ImageGrab.grab()
        screenshot_image = np.array(screenshot)
        is_dead = self.death_parser.parse_image(screenshot_image)
        if is_dead:
            print("DeadParser: Player dead")
            self.player.play_warning()
