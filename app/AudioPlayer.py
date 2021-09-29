# import winsound

class AudioPlayer:
    def __init__(self, captcha_file, warning_file):
        self.captcha_audio = captcha_file
        self.warning_audio = warning_file

    def play_captcha(self):
        # winsound.PlaySound(self.captcha_audio, winsound.SND_ASYNC)
        pass

    def play_warning(self):
        # winsound.PlaySound(self.warning_audio, winsound.SND_ASYNC)
        pass

    def stop_all(self):
        # winsound.PlaySound(None, winsound.SND_PURGE)
        pass
