import sys
import time
from threading import Thread

from infi.systray import SysTrayIcon

from win32gui import GetWindowText, GetForegroundWindow


class Ui:
    is_stop = True
    app_name = None
    app_icon = None
    app_menu_options = None
    captcha_parser = None

    def __init__(self, app_name, app_icon, app_player, logic):
        self.app_name = app_name
        self.icon = app_icon
        self.logic = logic
        self.app_menu_options = (("Start/Stop", None, app_pause),
                                 ("Test audio", None, app_test_audio),
                                 ("Stop audio", None, app_stop_audio))
        self.app_player = app_player
        global app
        app = self

    def start_ui(self):
        SysTrayIcon(self.app_icon, "%s - On Pause" % self.app_name, self.app_menu_options, on_quit=app_destroy).start()
        pass

    def start_captcha(self):
        Thread(target=self._lop).start()

    def stop_captcha(self):
        self.is_stop = True

    def _lop(self):
        while not self.is_stop:
            if GetWindowText(GetForegroundWindow()) != "Lineage II":
                print("No game found, waiting for it, %s" % GetWindowText(GetForegroundWindow()))
            else:
                captcha_button = self.logic.check_captcha()
                if captcha_button is not None:
                    self.app_player.play_captcha()
                    self.logic.apply_click(captcha_button)
                else:
                    print("Loop: Captcha answer is %s" % captcha_button)

            time.sleep(2)
        print("Loop stopped")


def app_pause(systray):
    app.is_stop = False if app.is_stop is True else True

    if app.is_stop is True:
        systray.update(hover_text="%s - On Pause" % app.app_name)
        app.stop_captcha()
        print("Paused")
    else:
        systray.update(hover_text=app.app_name)
        app.stop_captcha()
        print("Resumed")


def app_stop_audio(systray):
    app.app_player.stop_all()


def app_test_audio(systray):
    app.app_player.play_captcha()


def app_destroy(systray):
    sys.exit()
