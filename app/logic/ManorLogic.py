import numpy as np
import pyautogui
from PIL import ImageGrab


class ManorLogic:
    def __init__(self, manor_parser):
        self.manor_parser = manor_parser

    def check_manor(self):
        screenshot = ImageGrab.grab()
        screenshot_image = np.array(screenshot)
        return self.manor_parser.parse_image(screenshot_image)

    def apply_move(self, button):
        pyautogui.moveTo(int(button[0]), int(button[1]))

    def apply_click(self, button=None):
        if button is None:
            pyautogui.mouseDown()
            pyautogui.mouseUp()
        else:
            pyautogui.mouseDown(int(button[0]), int(button[1]))
            pyautogui.mouseUp(int(button[0]), int(button[1]))
