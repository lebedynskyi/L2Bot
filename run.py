import logging
import os
import sys
from logging.handlers import RotatingFileHandler

from app.base import BaseApp
from app.keyboard import ArduinoKeyboard
from app.template import GraciaRebornTemplates

logger = logging.getLogger()
l2_window = None


def init_logger():
    if not os.path.exists("res/output/logs"):
        os.mkdir("res/output/logs")

    formatter = logging.Formatter(fmt="%(asctime)s: %(name)s: %(message)s")
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.level = logging.DEBUG
    console_handler.setFormatter(formatter)

    file_handler = RotatingFileHandler(filename='res/output/logs/l2auto.log', maxBytes=1 * 1024 * 1024,
                                       mode='a', backupCount=5, encoding="utf-8", delay=False)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    logging.basicConfig(encoding="utf-8", level=logging.DEBUG, handlers=[console_handler, file_handler])
    logging.getLogger("PIL.PngImagePlugin").setLevel(logging.INFO)

    logger.info("Init logger OK")


def check_dependencies():
    import pytesseract
    tes_version = pytesseract.get_tesseract_version()
    logger.info("Tesseract version is %s", tes_version)

    import cv2
    cv_version = cv2.__version__
    logger.info("OpenCv version is %s", cv_version)

    # import PySide6.QtCore
    # qt_version = PySide6.__version__
    # logger.info("QT version is %s", qt_version)
    logger.info("Check Dependencies OK")


def has_admin_right():
    try:
        import ctypes
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def find_l2_window():
    import win32gui
    win32gui.EnumWindows(find_l2_window_callback, None)


def find_l2_window_callback(hwnd, extra):
    import win32gui
    rect = win32gui.GetWindowRect(hwnd)
    x = rect[0]
    y = rect[1]
    w = rect[2] - x
    h = rect[3] - y
    title = win32gui.GetWindowText(hwnd)
    if "lineage ii" == title.lower():
        logger.info("Lineage 2 window found")
        logger.info("\tLocation: (%d, %d)", x, y)
        logger.info("\tSize: (%d, %d)", w, h)
        global l2_window
        l2_window = hwnd
        logger.info("Check Dependencies OK")


if __name__ == "__main__":
    print("--------------  Welcome to Vetalll bot --------------  ")

    init_logger()
    check_dependencies()
    keyboard = ArduinoKeyboard("COM3")

    gracia_templates = GraciaRebornTemplates("res/templates")

    if not os.name == 'nt':
        logger.error("Finish app due to invalid OS")
        exit(1)

    if not has_admin_right():
        logger.error("Finish app due to  lack of admin rights")
        exit(1)

    find_l2_window()
    if not l2_window:
        logger.error("Finish app due to  l2 Window not found")
        exit(1)

    from app.capture_tmep import WinCap
    wincap = WinCap(l2_window)
    app = BaseApp(wincap)
    app.loop()

    logger.info("Finish app")
