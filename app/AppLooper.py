import time

import numpy as np
from PIL import ImageGrab


class AppLooper:
    def __init__(self, handlers):
        self.handlers = handlers
        pass

    def loop(self):
        while True:
            screenshot = ImageGrab.grab()
            screen_rgb = np.array(screenshot)
            current_time = time.time()
            for handler in self.handlers:
                handler.on_tick(screen_rgb, current_time)

            time.sleep(0.5)
