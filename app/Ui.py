import sys
import time
from threading import Thread

from infi.systray import SysTrayIcon

from win32gui import GetWindowText, GetForegroundWindow


class Ui:
    is_stop = False
    app_name = None
    app_icon = None
    app_menu_options = None
    captcha_parser = None

    def __init__(self, app_name, app_icon, captcha_logic, user_logic):
        self.app_name = app_name
        self.icon = app_icon
        self.captcha_logic = captcha_logic
        self.user_logic = user_logic
        self.app_menu_options = (("Start/Stop", None, app_pause),
                                 ("Play audio", None, app_test_audio),
                                 ("Stop audio", None, app_stop_audio))
        global app
        app = self

    def start_ui(self):
        SysTrayIcon(self.app_icon, "%s - On Pause" % self.app_name, self.app_menu_options, on_quit=app_destroy).start()
        self.start_captcha()
        pass

    def start_captcha(self):
        Thread(target=self._lop).start()

    def stop_captcha(self):
        self.is_stop = True

    def _lop(self):
        while not self.is_stop:
            try:
                captcha_button = self.captcha_logic.check_captcha()
                if captcha_button is not None:
                    self.captcha_logic.apply_click(captcha_button)
                else:
                    print("Loop: No Bot captcha found")

                hp_coef = self.user_logic.check_user_status()
                print("HP Coeff -> %s " % hp_coef)
            except BaseException as e:
                print("Error during making screenshot")
                print(e)
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
        app.start_captcha()
        print("Resumed")


def app_stop_audio(systray):
    app.captcha_logic.player.stop_all()


def app_test_audio(systray):
    app.captcha_logic.player.play_warning()


def app_destroy(systray):
    sys.exit()
