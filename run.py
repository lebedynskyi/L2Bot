import logging
import os
import sys
import time
from logging.handlers import RotatingFileHandler

from src.app import ClassicEveFarmApp

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


if __name__ == "__main__":
    print("--------------  Welcome to Vetalll bot --------------  ")
    init_logger()
    check_dependencies()

    time.sleep(3)

    ClassicEveFarmApp("Taro").loop()
