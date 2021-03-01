import os
from app.App import App
from app.AntiBotParser import AntiBotParser

env_path = os.path.dirname(os.path.realpath(__file__))
capture_file_path = os.path.join(env_path, "screen.png")

app = App(capture_file_path)


def loop():
    app.tick()


if __name__ == "__main__":
    p = AntiBotParser()

    input = os.path.join(env_path, "input", "3.bmp")
    template = os.path.join(env_path, "template", "captcha_bot.png")
    p.parse(input, template)
