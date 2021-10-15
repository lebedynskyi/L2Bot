import os

import cv2

from app.AppLooper import AppLooper
from app.handlers.Buff import BuffHandler
from app.handlers.Captcha import CaptchaHandler
from app.handlers.IntelligentFarm import IntelligentFarmHandler
from app.handlers.Manor import ManorSellCastle, ManorHandler
from app.handlers.PetManaKiller import PetManaHandler
from app.handlers.UserDeath import UserDeathHandler
from app.handlers.UserTeleported import UserTeleportedHandler
from app.parsers.ColorParser import ColorParser
from app.parsers.captcha.GroupDialogParser import GroupDialogParser
from app.parsers.DialogParsers import WarnDialogParser, DialogContentParser
from app.parsers.farm.TargetHpParser import TargetHpParser
from app.parsers.farm.TargetWindowParser import TargetWindowParser
from app.parsers.manor.CastlesListChooserParser import CastlesListChooserParser
from app.parsers.manor.CastlesListParser import CastlesListParser
from app.parsers.manor.CropListParser import CropListParser
from app.parsers.manor.ManorDialogParser import ManorDialogParser
from app.parsers.status.UserDeathStatusParser import UserDeathStatusParser
from app.parsers.status.UserStatusParser import UserStatusParser
from app.solver.CaptchaSolver import CaptchaSolver

env_path = os.path.dirname(os.path.realpath(__file__))


def manor_app():
    castles = [
        ManorSellCastle("Aden", "Fake", start_index=4, castle_number=2),
        ManorSellCastle("Rune", "Fake", start_index=4)
    ]

    manor_dialog_template = cv2.imread("res/template/manor/manor_template_1.png")
    manor_dialog_parser = ManorDialogParser(env_path, manor_dialog_template)

    crop_list_template = cv2.imread("res/template/manor/crop_sales_dialog.png")
    crop_list_parser = CropListParser(env_path, crop_list_template)

    castles_list_template = cv2.imread("res/template/manor/chooser_template.png")
    castles_list_parser = CastlesListParser(env_path, castles_list_template)

    castles_chooser_parser_template = cv2.imread("res/template/manor/chooser_expanded_template.png")
    castles_chooser_parser = CastlesListChooserParser(env_path, castles_chooser_parser_template)

    manor = ManorHandler(castles, manor_dialog_parser, crop_list_parser, castles_list_parser, castles_chooser_parser)
    looper = AppLooper(manor, tick_delay=-1)
    looper.loop()


def farm_app():
    warn_template = cv2.imread("res/template/warning_template.png")
    warn_dialog_parser = WarnDialogParser(env_path, warn_template)

    group_template = cv2.imread("res/template/dualbox_template.png")
    group_captcha_parser = GroupDialogParser(env_path, group_template)

    death_template = cv2.imread("res/template/status/user_death_template.png")
    death_parser = UserDeathStatusParser(env_path, death_template)

    target_template = cv2.imread("res/template/farm/target_template.png")
    target_window_parser = TargetWindowParser(env_path, target_template)

    status_template = cv2.imread("res/template/status/user_status_template.png")
    status_parser = UserStatusParser(env_path, status_template)

    dialog_content_parser = DialogContentParser(env_path)
    captcha_solver = CaptchaSolver()

    color_parser = ColorParser(env_path, 20)

    captcha = CaptchaHandler(warn_dialog_parser, dialog_content_parser, group_captcha_parser, captcha_solver)
    death = UserDeathHandler(death_parser)
    farm = IntelligentFarmHandler(target_window_parser, TargetHpParser(env_path))
    pet = PetManaHandler(status_parser, farm)
    buff = BuffHandler()
    teleport = UserTeleportedHandler(color_parser,handlers_to_pause=[pet, buff, death])

    looper = AppLooper(buff, captcha, death, pet, teleport)
    # looper = AppLooper(teleport)
    looper.loop()


if __name__ == "__main__":
    farm_app()
    # manor_app()
