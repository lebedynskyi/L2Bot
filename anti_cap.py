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

    template = os.path.join(env_path, "template", "captcha_bot.png")
    for f in os.listdir(os.path.join(env_path, "input")):
        p.parse(os.path.join(env_path, "input", f), template)
