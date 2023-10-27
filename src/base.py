import logging
import random
import time
from abc import ABC, abstractmethod

import cv2
import numpy as np
from PIL import Image

logger = logging.getLogger("BaseApp")


class Capture(ABC):
    hwnd = None
    offset_x = 0
    offset_y = 0
    w = 0
    h = 0
    center = (0, 0)

    @abstractmethod
    def screenshot(self):
        pass


class MockCap(Capture):
    def __init__(self, *screen_files):
        self.screen_files = screen_files

    def screenshot(self):
        random_index = random.randrange(len(self.screen_files))
        return Image.open(self.screen_files[random_index])


class BaseApp:
    def __init__(self, capture: Capture, tick_delay_seconds=3, handlers=[]):
        self.handlers = handlers
        self.capture = capture
        self.tick_delay = tick_delay_seconds

    def loop(self):
        while True:
            try:
                screenshot = self.capture.screenshot()
                screen_bgr = np.array(screenshot)
                screen_rgb = cv2.cvtColor(screen_bgr, cv2.COLOR_BGR2RGB)
                screen_grey = cv2.cvtColor(screen_rgb, cv2.COLOR_BGR2GRAY)
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
