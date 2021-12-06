import os
import time

from app.core.controls import SoftKeyboard
from app.handlers.Captcha import CaptchaHandler
from app.handlers.PetManaKiller import PetManaHandler
from app.handlers.buff import UseBottlesHandler, SelfBuffHandler
from app.handlers.UserDeath import UserDeathHandler
from app.handlers.farm import SpoilManorFarmHandler
from app.core.looper import AppLooper
from app.core.templates import load_templates
from app.parsers.reborn_classic.target import TargetWindowParser
from app.parsers.reborn_classic.target import TargetHpParser
from app.parsers.reborn_classic.ui import WarnDialogParser, GroupDialogParser
from app.parsers.reborn_classic.player import UserDeathStatusParser, UserStatusParser
from app.parsers.text import DialogTextParser
from app.solver.CaptchaSolver import CaptchaSolver

env_path = os.path.dirname(os.path.realpath(__file__))


def farm_osx_app():
    keyboard = SoftKeyboard()
    keyboard.init(0.1)

    templates = load_templates("res/template/reborn_classic")
    hp_parser = UserStatusParser(env_path, templates.status.user_status)
    target_window_parser = TargetWindowParser(env_path, templates.farm.target)
    target_hp_parser = TargetHpParser(env_path)
    warn_dialog_parser = WarnDialogParser(env_path, templates.captcha.warn_dialog)
    group_captcha_dialog_parser = GroupDialogParser(env_path, templates.captcha.dualbox_dialog)
    dialog_text_parser = DialogTextParser(env_path)
    solver = CaptchaSolver()
    user_death_parser = UserDeathStatusParser(env_path, templates.status.user_death)

    bottles = UseBottlesHandler(keyboard)
    captcha = CaptchaHandler(keyboard, warn_dialog_parser, dialog_text_parser, group_captcha_dialog_parser, solver)
    death = UserDeathHandler(keyboard, user_death_parser)

    farm = SpoilManorFarmHandler(keyboard, target_window_parser, target_hp_parser,
                                 use_skills=False, use_manor=True, use_spoil=False)
    pet_killer = PetManaHandler(keyboard, hp_parser, farm)
    self_buff = SelfBuffHandler(keyboard, farm, [farm, pet_killer])
    return AppLooper(death, captcha, self_buff, farm, pet_killer)
    # return AppLooper(captcha)


if __name__ == "__main__":
    time.sleep(1)
    # farm_app().loop()
    farm_osx_app().loop()