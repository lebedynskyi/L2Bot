import logging
import os
from ctypes import windll

import cv2
import numpy as np
import win32gui
import win32ui
from PIL import Image

from src.base import Capture

logger = logging.getLogger("WinCap")


class WinCap(Capture):
    hwnd = None

    def __init__(self, window_name):
        if not os.name == 'nt':
            logger.error("Finish app due to invalid OS")
            exit(1)

        if not has_admin_right():
            logger.error("Finish app due to lack of admin rights")
            exit(1)

        self._find_l2_window(window_name)

        if self.hwnd is None:
            logger.error("Finish app due to l2 Window not found")
            exit(1)

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
        success = windll.user32.PrintWindow(self.hwnd, saveDC.GetSafeHdc(), 0)

        bmpinfo = saveBitMap.GetInfo()
        bmpstr = saveBitMap.GetBitmapBits(True)

        screenshot = Image.frombuffer(
            'RGB',
            (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
            bmpstr, 'raw', 'BGRX', 0, 1)

        win32gui.DeleteObject(saveBitMap.GetHandle())
        saveDC.DeleteDC()
        mfcDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, hwndDC)

        screen_bgr = np.array(screenshot)
        screen_rgb = cv2.cvtColor(screen_bgr, cv2.COLOR_BGR2RGB)
        screen_grey = cv2.cvtColor(screen_rgb, cv2.COLOR_BGR2GRAY)
        return screen_rgb, screen_grey

    def _find_l2_window(self, win_name):
        def callback(hwnd, extra):
            title = win32gui.GetWindowText(hwnd)
            if win_name.lower() in title.lower():
                logger.info("Lineage 2 window found. Full name - %s", title)
                self.hwnd = hwnd

        win32gui.EnumWindows(callback, None)

    # get the window size and position
    def _update_window_position(self):
        import win32gui
        window_rect = win32gui.GetWindowRect(self.hwnd)

        w = window_rect[2] - window_rect[0]
        h = window_rect[3] - window_rect[1]

        # account for the window border and titlebar and cut them off
        border_pixels = 8
        titlebar_pixels = 30
        self.w = w - (border_pixels * 2)
        self.wh = h - titlebar_pixels - border_pixels

        # set the cropped coordinates offset so we can translate screenshot
        # images into actual screen positions
        self.offset_x = window_rect[0]
        self.offset_y = window_rect[1]
        self.center = (w / 2, h / 2)

        logger.debug("Updated l2 window coordinates, w=%s, h=%s, offset_x=%s, offset_y=%s",
                     self.w, self.h, self.offset_x, self.offset_y)


def has_admin_right():
    try:
        import ctypes
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False
