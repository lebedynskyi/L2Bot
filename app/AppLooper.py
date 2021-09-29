import time

import numpy as np
import pyautogui
from PIL import ImageGrab


class AppLooper:
    def __init__(self, handlers):
        self.handlers = handlers
        pass

    def loop(self):
        pyautogui.FAILSAFE = False
        while True:
            screenshot = ImageGrab.grab()
            array = np.array(screenshot)
            current_time = time.time()
            for handler in self.handlers:
                handler.on_tick(array, current_time)

            time.sleep(0.5)
