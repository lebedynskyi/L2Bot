import os
import time

from app.core.controls import ArduinoKeyboard
from app.core.looper import AppLooper
from app.core.templates import load_templates
from app.handlers.farm import SpoilManorFarmHandler
from app.parsers.classic.target import TargetWindowParser
from app.parsers.classic.target import TargetHpParser

env_path = os.path.dirname(os.path.realpath(__file__))


def farm_app():
    keyboard = ArduinoKeyboard()
    keyboard.init()

    templates = load_templates("res/template/classic")
    target_window_parser = TargetWindowParser(env_path, templates.farm.target)
    target_hp_parser = TargetHpParser(env_path)

    farm = SpoilManorFarmHandler(keyboard, target_window_parser, target_hp_parser,
                                 use_skills=False, use_manor=True, use_spoil=False)
    return AppLooper(farm)


if __name__ == "__main__":
    time.sleep(5)
    farm_app().loop()
