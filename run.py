import os
import time

from app.core.controls import ArduinoKeyboard
from app.handlers.Captcha import CaptchaHandler
from app.handlers.Manor import ManorSellCastle, ManorHandler
from app.handlers.PetManaKiller import PetManaTimerHandler
from app.handlers.buff import UseBottlesHandler, SelfBuffHandler
from app.handlers.UserDeath import UserDeathHandler
from app.handlers.farm import SpoilManorFarmHandler
from app.core.looper import AppLooper
from app.core.templates import load_templates
from app.parsers.classic.manor import ManorDialogParser, CropListParser, CastlesListParser, CastlesListChooserParser
from app.parsers.classic.target import TargetWindowParser
from app.parsers.classic.target import TargetHpParser
from app.parsers.classic.ui import WarnDialogParser, GroupDialogParser
from app.parsers.text import DialogTextParser
from app.solver.CaptchaSolver import CaptchaSolver
from app.parsers.reborn_classic.player import UserDeathStatusParser

env_path = os.path.dirname(os.path.realpath(__file__))


def spoil_manor_app():
    keyboard = ArduinoKeyboard()
    keyboard.init(0.1)

    templates = load_templates("res/template/classic")
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
                                 use_skills=True, use_manor=True, use_spoil=True)
    return AppLooper(death, captcha, farm, bottles)


def captcha_app():
    keyboard = ArduinoKeyboard()
    keyboard.init(0.1)
    templates = load_templates("res/template/classic")
    warn_dialog_parser = WarnDialogParser(env_path, templates.captcha.warn_dialog)
    group_captcha_dialog_parser = GroupDialogParser(env_path, templates.captcha.warn_dialog)
    dialog_text_parser = DialogTextParser(env_path)
    solver = CaptchaSolver()
    captcha = CaptchaHandler(keyboard, warn_dialog_parser, dialog_text_parser, group_captcha_dialog_parser, solver)
    return AppLooper(captcha)


def farm_pp_app():
    keyboard = ArduinoKeyboard()
    keyboard.init(0.1)

    templates = load_templates("res/template/classic")
    target_window_parser = TargetWindowParser(env_path, templates.farm.target)
    target_hp_parser = TargetHpParser(env_path)
    warn_dialog_parser = WarnDialogParser(env_path, templates.captcha.warn_dialog)
    group_captcha_dialog_parser = GroupDialogParser(env_path, templates.captcha.warn_dialog)
    dialog_text_parser = DialogTextParser(env_path)
    solver = CaptchaSolver()
    user_death_parser = UserDeathStatusParser(env_path, templates.status.user_death)

    captcha = CaptchaHandler(keyboard, warn_dialog_parser, dialog_text_parser, group_captcha_dialog_parser, solver)
    death = UserDeathHandler(keyboard, user_death_parser)
    farm = SpoilManorFarmHandler(keyboard, target_window_parser, target_hp_parser,
                                 use_skills=False, use_manor=True, use_spoil=False)
    pet_killer = PetManaTimerHandler(keyboard, farm)
    self_buff = SelfBuffHandler(keyboard, farm, [farm, pet_killer])
    return AppLooper(death, captcha, self_buff, pet_killer, farm)


def manor_app():
    keyboard = ArduinoKeyboard()
    keyboard.init(0.01)

    templates = load_templates("res/template/classic")

    castles = [
        ManorSellCastle("Goddard", "Fake", start_index=2, castle_number=5)
        # ManorSellCastle("Gludio", "Gludio", start_index=2, castle_number=2)
        # ManorSellCastle("Oren", "Giran", start_index=2, castle_number=3)
    ]

    manor_dialog_parser = ManorDialogParser(env_path, templates.manor.manor_dialog_template)
    crop_list_parser = CropListParser(env_path, templates.manor.crop_sales_dialog)
    castles_list_parser = CastlesListParser(env_path, templates.manor.chooser_template)
    castles_chooser_parser = CastlesListChooserParser(env_path, templates.manor.chooser_expanded_template)
    manor = ManorHandler(keyboard, castles,
                         manor_dialog_parser, crop_list_parser, castles_list_parser, castles_chooser_parser)
    return AppLooper(manor, tick_delay=-1)


if __name__ == "__main__":
    time.sleep(1)
    # app = spoil_manor_app()
    # app = captcha_app()
    app = farm_pp_app()
    # app = manor_app()

    app.loop()
