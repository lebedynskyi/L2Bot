import os
import time

import cv2

from app.AppLooper import AppLooper
from app.logic.BuffLogic import BuffLogic
from app.logic.CaptchaLoigic import CaptchaLogic
from app.logic.FarmLogic import FarmLogic
from app.logic.ManorLogic import SellCastle, ManorLogic
from app.logic.PetManaLogic import PetManaLogic
from app.logic.UserDeathLogic import UserDeathLogic
from app.parsers.captcha.BotCaptcha import BotCaptchaParser
from app.parsers.captcha.GroupDialogParser import GroupDialogParser
from app.parsers.captcha.WarnDialog import WarnDialogParser
from app.parsers.farm.TargetParser import TargetParser
from app.parsers.manor.CastlesListChooserParser import CastlesListChooserParser
from app.parsers.manor.CastlesListParser import CastlesListParser
from app.parsers.manor.CropListParser import CropListParser
from app.parsers.manor.ManorDialogParser import ManorDialogParser
from app.parsers.status.UserDeathStatusParser import UserDeathStatusParser
from app.parsers.status.UserStatusParser import UserStatusParser
from app.solver.CaptchaSolver import CaptchaSolver

env_path = os.path.dirname(os.path.realpath(__file__))


def manor_app():
    time.sleep(4)
    castles = [
        SellCastle("Aden", "Fake", start_index=2),
        SellCastle("Aden", "Fake", start_index=2)
    ]

    manor_dialog_template = cv2.imread("res/template/manor/manor_template_1.png")
    manor_dialog_parser = ManorDialogParser(env_path, manor_dialog_template)

    crop_list_template = cv2.imread("res/template/manor/crop_sales_dialog.png")
    crop_list_parser = CropListParser(env_path, crop_list_template)

    castles_list_template = cv2.imread("res/template/manor/chooser_template.png")
    castles_list_parser = CastlesListParser(env_path, castles_list_template)

    castles_chooser_parser_template = cv2.imread("res/template/manor/chooser_expanded_template.png")
    castles_chooser_parser = CastlesListChooserParser(env_path, castles_chooser_parser_template)

    manor = ManorLogic(castles, manor_dialog_parser, crop_list_parser, castles_list_parser, castles_chooser_parser)
    looper = AppLooper(manor, tick_delay=-1)
    looper.loop()


def farm_app():
    warn_template = cv2.imread("res/template/warning_template.png")
    dialog_parser = WarnDialogParser(env_path, warn_template)

    group_template = cv2.imread("res/template/dualbox_template.png")
    group_captcha_parser = GroupDialogParser(env_path, group_template)

    death_template = cv2.imread("res/template/status/user_death_template.png")
    death_parser = UserDeathStatusParser(env_path, death_template)

    target_template = cv2.imread("res/template/farm/target_template.png")
    target_parser = TargetParser(env_path, target_template)

    status_template = cv2.imread("res/template/status/user_status_template.png")
    status_parser = UserStatusParser(env_path, status_template)

    captcha_parser = BotCaptchaParser(env_path)
    captcha_solver = CaptchaSolver()

    captcha = CaptchaLogic(dialog_parser, captcha_parser, group_captcha_parser, captcha_solver)
    death = UserDeathLogic(death_parser)
    farm = FarmLogic(target_parser)
    pet = PetManaLogic(status_parser, farm)
    buff = BuffLogic()

    looper = AppLooper(captcha, death, farm, pet, buff)
    looper.loop()


if __name__ == "__main__":
    farm_app()
    # manor_app()

    pass
