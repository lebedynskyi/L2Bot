import os
import cv2

from app.AppLooper import AppLooper
from app.logic.CaptchaLoigic import CaptchaLogic
from app.logic.FarmLogic import FarmLogic
from app.logic.UserDeathLogic import UserDeathLogic
from app.logic.UserStatusLogic import UserStatusLogic
from app.parsers.captcha.BotCaptcha import BotCaptchaParser
from app.parsers.captcha.GroupDialogParser import GroupDialogParser
from app.parsers.captcha.WarnDialog import WarnDialogParser
from app.parsers.farm.TargetParser import TargetParser
from app.parsers.status.UserDeathStatusParser import UserDeathStatusParser
from app.parsers.status.UserStatusParser import UserStatusParser
from app.solver.CaptchaSolver import CaptchaSolver

env_path = os.path.dirname(os.path.realpath(__file__))


def loop_spoil_farm():
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
    status = UserStatusLogic(status_parser)

    looper = AppLooper([captcha, death, farm, status])
    looper.loop()


if __name__ == "__main__":
    loop_spoil_farm()
