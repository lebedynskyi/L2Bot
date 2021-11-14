import os

from app.core.looper import AppLooper
from app.core.templates import load_templates
from app.handlers.OrcShamanFarm import OrcShamanFarmHandler
from app.parsers.farm.TargetHpParser import TargetHpParser
from app.parsers.farm.TargetWindowParser import TargetWindowParser

env_path = os.path.dirname(os.path.realpath(__file__))


def farm_app():
    templates = load_templates("res/template/interlude")
    target_window_parser = TargetWindowParser(env_path, templates.farm.target)
    target_hp_parser = TargetHpParser(env_path)

    farm = OrcShamanFarmHandler(target_window_parser, target_hp_parser, use_manor=False)
    return AppLooper(farm)


if __name__ == "__main__":
    farm_app().loop()
