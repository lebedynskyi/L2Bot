import logging
import random
import threading
import time
from abc import ABC, abstractmethod

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
    def screenshot(self) -> int:
        raise NotImplementedError("screenshot() is not implemented for base  Capture class")


class MockCap(Capture):
    def __init__(self, *screen_files):
        self.screen_files = screen_files

    def screenshot(self):
        random_index = random.randrange(len(self.screen_files))
        return Image.open(self.screen_files[random_index])


class Looper:
    logger = logging.getLogger("Looper")
    thread_lock = threading.Condition()

    active = True
    exit = False
    thread = None

    def __init__(self, *handlers, tick_delay=0.5):
        self.tick_delay = tick_delay
        self.handlers = handlers

    def start(self):
        self.thread = threading.Thread(name="BotLooper", target=self._loop)
        self.thread.start()
        self.thread.join()

    def stop(self):
        self.logger.info("Stop")
        self.exit = True

        if not self.active:
            self.active = True
            self._release_lock()

    def toggle_pause(self):
        self.active = not self.active
        if self.active:
            self.logger.info("Resume loop")
        else:
            self.logger.info("Pause loop")

        self._release_lock()

    def _loop(self):
        self.logger.debug("Start loop")

        while True:
            if not self.active:
                self.logger.debug("Looper is paused. Sleep")
                self._wait_lock()
                self.logger.debug("Looper is resumed. Wake UP")

            if self.exit:
                exit(0)

            if self.active:
                for h in self.handlers:
                    self._on_tick_handler(h)

                if self.tick_delay > 0:
                    time.sleep(self.tick_delay)

    def _wait_lock(self):
        self.thread_lock.acquire()
        self.thread_lock.wait()
        self.thread_lock.release()

    def _release_lock(self):
        self.thread_lock.acquire()
        self.thread_lock.notify_all()
        self.thread_lock.release()

    def _on_tick_handler(self, h):
        try:
            h.on_tick(time.time())
        except BaseException as e:
            self.logger.exception("Error during tick in %s. Error -> %s", h.__class__.__name__, e)
