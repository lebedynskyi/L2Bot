import logging
import os
import sys
import time
from logging.handlers import RotatingFileHandler

from pynput import keyboard

from src.app import farm_app, manor_app
from src.base import Looper

DEVELOP = True
logger = logging.getLogger()


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

    logger.info("Check Dependencies OK")


def register_hotkeys(toggle_callback, exit_callback):
    keys = set()

    def on_press(key):
        try:
            keys.add(key.char)
            if (key.char == "s" or key.char == "S") and (
                    keyboard.Key.alt in keys or keyboard.Key.alt_l in keys or keyboard.Key.alt_r in keys):
                toggle_callback()
            if (key.char == "q" or key.char == "Q") and (
                    keyboard.Key.alt in keys or keyboard.Key.alt_l in keys or keyboard.Key.alt_r in keys):
                exit_callback()
        except AttributeError:
            keys.add(key)
        except KeyError as e:
            logger.debug("Unknown key pressed, %s, Error %s", key, e)

    def on_release(key):
        try:
            keys.remove(key.char)
        except AttributeError:
            keys.remove(key)
        except KeyError as e:
            logger.debug("Unknown key release, %s, Error %s", key, e)

    listener = keyboard.Listener(
        on_press=on_press,
        on_release=on_release)
    listener.start()


if __name__ == "__main__":
    init_logger()
    check_dependencies()
    # looper = Looper(*farm_app("Taro"))
    looper = Looper(*manor_app("Lineage II"), tick_delay=0)

    register_hotkeys(
        toggle_callback=lambda: looper.toggle_pause(),
        exit_callback=lambda: looper.stop()
    )

    print("--------------  Welcome to Vetalll bot --------------")
    print("--------------  Press 'ALT + s/S' to start/pause --------------")
    print("--------------  Press 'ALT + q/Q' to stop/exit --------------")

    looper.start()
