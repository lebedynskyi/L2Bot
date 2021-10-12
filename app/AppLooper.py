import time
import traceback
import numpy as np

from PIL import ImageGrab


class AppLooper:
    def __init__(self, *handlers, tick_delay=1):
        self.tick_delay = tick_delay
        self.handlers = handlers

    def loop(self):
        time.sleep(4)

        while True:
            screenshot = None
            try:
                screenshot = ImageGrab.grab()
            except BaseException:
                print("AppLooper: cannot make screenshot")
                print(traceback.format_exc())

            array = np.array(screenshot)
            current_time = time.time()
            for handler in self.handlers:
                try:
                    handler.on_tick(array, current_time)
                except BaseException:
                    print("AppLooper: exception in handler {}".format(handler))
                    print(traceback.format_exc())

            if self.tick_delay > 0:
                time.sleep(self.tick_delay)

            print("\r")
