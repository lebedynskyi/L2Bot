import logging
import os
import sys
import time
from logging.handlers import RotatingFileHandler

from src.base import BaseApp
from src.bot.spoiler import HandlerSpoilerAutoFarm, ControllerSpoilerAutoFarm
from src.capture import MockCap
from src.keyboard import ArduinoKeyboard, BaseKeyboard
from src.parser.c3 import C3NearTargetsParser, C3TargetParser
from src.template import C3Templates

DEVELOP = False
logger = logging.getLogger()
l2_window = None


def init_logger():
    if not os.path.exists("res/output/logs"):
        os.mkdir("res/output/logs")

    formatter = logging.Formatter(fmt="%(asctime)s: %(name)s: %(message)s")
    console_handler = logging.StreamHandler(sys.stdout)
    if DEVELOP:
        console_handler.level = logging.DEBUG
    else:
        console_handler.level = logging.INFO
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


def initialize_on_windows():
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


def run_manor_trade():
    pass


def run_farm():
    initialize_on_windows()
    import src.capture as capture
    wincap = capture.WinCap(l2_window)

    keyboard = ArduinoKeyboard(port="COM3")
    controller_spoil_auto_farm = ControllerSpoilerAutoFarm(keyboard, wincap)

    c3_templates = C3Templates("res/templates")

    parser_near_target = C3NearTargetsParser()
    parser_target = C3TargetParser(c3_templates)
    handler_spoil_auto_farm = HandlerSpoilerAutoFarm(controller_spoil_auto_farm,
                                                     parser_near_target, parser_target,
                                                     "Gremlin")

    app = BaseApp(wincap, handler_spoil_auto_farm, tick_delay_seconds=0.8)
    app.loop()


def run_develop():
    mock_cap = MockCap("res/input/c3/Shot00004.bmp", "res/input/c3/Shot00008.bmp")
    parser_near_target = C3NearTargetsParser()
    BaseKeyboard()
    handler_spoil_auto_farm = HandlerSpoilerAutoFarm(None, parser_near_target, "Goblin Snooper")
    app = BaseApp(mock_cap, handler_spoil_auto_farm)
    app.loop()
    logger.info("Finish due to develop")


if __name__ == "__main__":
    print("--------------  Welcome to Vetalll bot --------------  ")
    init_logger()
    check_dependencies()

    if DEVELOP:
        run_develop()
    else:
        time.sleep(3)
        run_farm()
        # run_manor_trade()
