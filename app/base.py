import logging
import time

import cv2
import numpy as np
from PIL import ImageGrab

logger = logging.getLogger("BaseApp")


class BaseApp:
    def __init__(self, *handlers, tick_delay_seconds=1):
        self.tick_delay = tick_delay_seconds
        self.handlers = handlers

    def loop(self):
        while True:
            try:
                screenshot = ImageGrab.grab()
                screen_bgr = np.array(screenshot)
                screen_rgb = cv2.cvtColor(screen_bgr, cv2.COLOR_BGR2RGB)
                screen_grey = cv2.cvtColor(screen_bgr, cv2.COLOR_BGR2GRAY)
            except Exception as e:
                logger.exception("Unable to take screenshot, %s", e)
                continue

            for h in self.handlers:
                try:
                    h.on_tick(screen_rgb, screen_grey, time.time())
                except Exception as e:
                    logger.exception("Error to handle tick in %s, %s", h.__class__.__name__, e)

            if self.tick_delay > 0:
                time.sleep(self.tick_delay)
