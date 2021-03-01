import pyautogui as gui


class Capture:
    def __init__(self):
        pass

    def capture(self, screenshot_uri):
        print("Making screenshot into -> %s" % screenshot_uri)
        gui.screenshot(screenshot_uri)
