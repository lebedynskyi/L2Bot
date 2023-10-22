import logging
import random
from abc import ABC, abstractmethod

from PIL import Image

logger = logging.getLogger("WinCap")


class Capture(ABC):
    @abstractmethod
    def screenshot(self):
        pass


class WinCap(Capture):
    hwnd = None
    cropped_x = 0
    cropped_y = 0
    offset_x = 0
    offset_y = 0
    w = 0
    h = 0

    def __init__(self, hwnd):
        from ctypes import windll

        self.windll = windll
        self.hwnd = hwnd
        self._update_window_position()

    def screenshot(self):
        left, top, right, bot = win32gui.GetWindowRect(self.hwnd)
        w = right - left
        h = bot - top

        hwndDC = win32gui.GetWindowDC(self.hwnd)
        mfcDC = win32ui.CreateDCFromHandle(hwndDC)
        saveDC = mfcDC.CreateCompatibleDC()

        saveBitMap = win32ui.CreateBitmap()
        saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)

        saveDC.SelectObject(saveBitMap)

        # Change the line below depending on whether you want the whole window
        # or just the client area.
        # result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 1)
        result = self.windll.user32.PrintWindow(self.hwnd, saveDC.GetSafeHdc(), 0)
        print
        result

        bmpinfo = saveBitMap.GetInfo()
        bmpstr = saveBitMap.GetBitmapBits(True)

        im = Image.frombuffer(
            'RGB',
            (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
            bmpstr, 'raw', 'BGRX', 0, 1)

        win32gui.DeleteObject(saveBitMap.GetHandle())
        saveDC.DeleteDC()
        mfcDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, hwndDC)
        return im

    # get the window size and position
    def _update_window_position(self):
        window_rect = win32gui.GetWindowRect(self.hwnd)
        w = window_rect[2] - window_rect[0]
        h = window_rect[3] - window_rect[1]

        # account for the window border and titlebar and cut them off
        border_pixels = 8
        titlebar_pixels = 30
        self.w = w - (border_pixels * 2)
        self.wh = h - titlebar_pixels - border_pixels
        self.cropped_x = border_pixels
        self.cropped_y = titlebar_pixels

        # set the cropped coordinates offset so we can translate screenshot
        # images into actual screen positions
        self.offset_x = window_rect[0] + self.cropped_x
        self.offset_y = window_rect[1] + self.cropped_y

        logger.debug("Updated l2 window coordinates, w=%s, h=%s, offset_x=%s, offset_y=%s",
                     self.w, self.h, self.offset_x, self.offset_y)


class MockCap(Capture):
    def __init__(self, *screen_files):
        self.screen_files = screen_files

    def screenshot(self):
        random_index = random.randrange(len(self.screen_files))
        return Image.open(self.screen_files[random_index])
