import os
from app.App import App
from app.AntiBotParser import AntiBotParser

env_path = os.path.dirname(os.path.realpath(__file__))
capture_file_path = os.path.join(env_path, "screen.png")

if __name__ == "__main__":
    icon_path = os.path.join(env_path, "res/app_ico.png")
    app = App("Antbl2", icon_path)
    app.run_app()

    # p = AntiBotParser()
    #
    # template = os.path.join(env_path, "template", "captcha_bot.png")
    # for f in os.listdir(os.path.join(env_path, "input")):
    #     p.parse(os.path.join(env_path, "input", f), template)

    # p.parse(os.path.join(env_path, "input", "Yes1.bmp"), template)
