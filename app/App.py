import sys
import os
import time
from datetime import datetime
from threading import Thread

from infi.systray import SysTrayIcon
from win10toast import ToastNotifier
from win32gui import GetWindowText, GetForegroundWindow, GetWindowRect
from PIL import ImageGrab

import numpy as np
import cv2

from app.AntiBotParser import AntiBotParser
from app.WarningPlayer import WarningPlayer

anti_bot_parser = AntiBotParser()


class App:
    is_stop = True
    flag_exit = False
    lastx = 0
    lasty = 0
    is_block = False
    new_cast_time = 0
    recast_time = 40
    wait_mes = 0

    name = None
    about = None
    icon_path = None
    menu_options = None

    def __init__(self, name, icon_path):
        self.toaster = ToastNotifier()
        self.name = name
        self.icon = icon_path
        self.process_thread = None
        self.menu_options = (("Start/Stop", None, app_pause),
                             ("Test audio", None, app_test_audio),
                             ("Stop audio", None, app_stop_audio))
        self.player = WarningPlayer(os.path.join("res/captcha_warn_long.wav"))
        global app
        app = self

    def run_app(self):
        tray = SysTrayIcon(self.icon_path, "%s - On Pause" % app.name, self.menu_options, on_quit=app_destroy).start()
        # self.toaster.show_toast(app.name, "Antbl2 started", icon_path=self.icon, duration=5)
        pass

    def start(self):
        self.process_thread = Thread(target=self._lop)
        self.process_thread.start()

    def stop(self):
        self.is_stop = True

    def _lop(self):
        while not self.is_stop:
            if GetWindowText(GetForegroundWindow()) != "Lineage II":
                print("No game found, wait for it, %s" % GetWindowText(GetForegroundWindow()))
                time.sleep(5)
            else:
                screenshot = ImageGrab.grab()
                game_image = np.array(screenshot)
                for t in os.listdir("res/template"):
                    dialog_template = cv2.imread(os.path.join("res/template", t))

                    if not dialog_template.data:
                        print("No template found. Skip")
                        continue

                    if not game_image.data:
                        print("No screenshot found. Skip")
                        continue

                    captcha_dialog = anti_bot_parser.find_captcha_dialog(game_image, dialog_template)
                    if captcha_dialog:
                        print("%s Captcha found" % datetime.now())
                        self.player.play_captcha()
                        cv2.imwrite(os.path.join("output/last_captcha.png"), game_image)
                        break
                else:
                    print("%s Captcha not found" % datetime.now())

            time.sleep(2.5)
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
    app.player.stop_all()


def app_test_audio(systray):
    app.player.play_captcha()


def app_destroy(systray):
    sys.exit()
