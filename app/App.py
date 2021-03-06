import sys
import os
import time
from datetime import datetime
from threading import Thread

import numpy as np
import cv2

from infi.systray import SysTrayIcon
from win32gui import GetWindowText, GetForegroundWindow
from PIL import ImageGrab

from app.AntiBotParser import AntiBotParser

anti_bot_parser = AntiBotParser()


class App:
    is_stop = True
    name = None
    about = None
    icon_path = None
    menu_options = None

    def __init__(self, name, icon_path, environment_path, app_player):
        self.name = name
        self.icon = icon_path
        self.env_paht = environment_path
        self.menu_options = (("Start/Stop", None, app_pause),
                             ("Test audio", None, app_test_audio),
                             ("Stop audio", None, app_stop_audio))
        self.app_player = app_player
        global app
        app = self

    def run(self):
        SysTrayIcon(self.icon_path, "%s - On Pause" % app.name, self.menu_options, on_quit=app_destroy).start()
        pass

    def start(self):
        Thread(target=self._lop).start()

    def stop(self):
        self.is_stop = True

    def _lop(self):
        while not self.is_stop:
            time.sleep(2.5)

            if GetWindowText(GetForegroundWindow()) != "Lineage II":
                print("No game found, wait for it, %s" % GetWindowText(GetForegroundWindow()))
            else:
                screenshot = ImageGrab.grab()
                game_image = np.array(screenshot)
                warning_template = cv2.imread("res/template/warning_template.png")

                if not warning_template.data:
                    print("No template found. Skip")
                    continue

                if not game_image.data:
                    print("No screenshot found. Skip")
                    continue

                has_captcha = anti_bot_parser.find_captcha_warning(game_image, warning_template)
                if has_captcha:
                    print("%s Found captcha warning " % datetime.now())
                    self.app_player.play_captcha()
                    cv2.imwrite(os.path.join("output/last_captcha_screenshot.png"), game_image)
                    continue

                for dialog in os.listdir("res/template/dialogs"):
                    dialog_template = cv2.imread(os.path.join("res/template/dialogs", dialog))
                    captcha_dialog = anti_bot_parser.find_captcha_dialog(game_image, dialog_template)
                    if captcha_dialog:
                        print("%s Found captcha dialog" % datetime.now())
                        self.app_player.play_captcha()
                        cv2.imwrite(os.path.join("output/last_captcha_dialog.png"), game_image)
                        break
                else:
                    print("%s Captcha not found" % datetime.now())

        print("Loop stopped")


def app_pause(systray):
    app.is_stop = False if app.is_stop is True else True

    if app.is_stop is True:
        systray.update(hover_text="%s - On Pause" % app.name)
        app.stop()
        print("Paused")
    else:
        systray.update(hover_text=app.name)
        app.start()
        print("Resumed")


def app_stop_audio(systray):
    app.app_player.stop_all()


def app_test_audio(systray):
    app.app_player.play_captcha()


def app_destroy(systray):
    sys.exit()
