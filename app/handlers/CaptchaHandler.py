from app.handlers.BaseHandler import BaseHandler


class CaptchaHandler(BaseHandler):
    def __init__(self, env_path, warn_dialog_handler):
        super().__init__(env_path)
        self.warn_dialog_handler = warn_dialog_handler

    def parse_image(self, image):
        warn_dialog = self.warn_dialog_handler.parse_image(image)

        if warn_dialog is not None:
            return self._find_captcha(warn_dialog)

    def _find_captcha(self, dialog):
        pass
