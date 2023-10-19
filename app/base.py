import logging
import time

import cv2
import numpy as np

logger = logging.getLogger("BaseApp")


class BaseApp:
    def __init__(self, wincap, *handlers, tick_delay_seconds=3):
        self.wincap = wincap
        self.tick_delay = tick_delay_seconds
        self.handlers = handlers

    def loop(self):
        while True:
            try:
                screenshot = self.wincap.screen1()
                screen_bgr = np.array(screenshot)
                screen_rgb = cv2.cvtColor(screen_bgr, cv2.COLOR_BGR2RGB)
                screen_grey = cv2.cvtColor(screen_rgb, cv2.COLOR_BGR2GRAY)

                cv2.imshow("Screenshot", screen_rgb)
                cv2.waitKey(0)
            except Exception as e:
                logger.exception("Unable to take screenshot, %s", e)
                self.wait_tick()
                continue

            for h in self.handlers:
                try:
                    h.on_tick(screen_rgb, screen_grey, time.time())
                except Exception as e:
                    logger.exception("Error to handle tick in %s, %s", h.__class__.__name__, e)

            self.wait_tick()

    def wait_tick(self):
        if self.tick_delay > 0:
            time.sleep(self.tick_delay)
