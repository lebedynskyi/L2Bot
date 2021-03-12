# import winsound
from playsound import playsound


class WarningPlayer:
    def __init__(self, captcha_file):
        self.captcha_audio = captcha_file

    def play_captcha(self):
        # winsound.PlaySound(self.captcha_audio, winsound.SND_ASYNC)
        playsound(self.captcha_audio)

    def stop_all(self):
        pass
        # winsound.PlaySound(None, winsound.SND_PURGE)
