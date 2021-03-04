from playsound import playsound
import winsound


class WarningPlayer:
    def __init__(self, captcha_file):
        self.captcha_audio = captcha_file

    def play_captcha(self):
        # playsound(self.captcha_audio)
        winsound.PlaySound(self.captcha_audio, winsound.SND_ASYNC)

    def stop_all(self):
        winsound.PlaySound(None, winsound.SND_PURGE)
