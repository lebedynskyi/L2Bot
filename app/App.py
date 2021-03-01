from app.Capture import Capture
from app.AntiBotParser import AntiBotParser


class App:
    def __init__(self, screen_path):
        self.screen_path = screen_path
        self.capture = Capture()
        self.parser = AntiBotParser()
        pass

    def register_handler(self):
        pass

    def tick(self):
        self.capture.capture(self.screen_path)
        data = self.parser.parse(self.screen_path)

    def _do_work(self, data):
        pass
