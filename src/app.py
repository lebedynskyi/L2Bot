from src.base import BaseApp
from src.bot.spoiler import ControllerSpoilerAutoFarm, HandlerSpoilerAutoFarm
from src.keyboard import ArduinoKeyboard
from src.parser.classic import ClassicNearTargetsParser, ClassicTargetParser
from src.template import ClassicTemplates
from src.win_capture import WinCap


class GraciaRebornFarmApp(BaseApp):
    def __init__(self, char_name):
        super().__init__(WinCap(char_name), 1, [])


class ClassicEveFarmApp(BaseApp):
    def __init__(self, char_name):
        win_cap = WinCap(char_name)
        keyboard = ArduinoKeyboard(port="COM3")
        controller_spoil_auto_farm = ControllerSpoilerAutoFarm(keyboard, win_cap)
        templates = ClassicTemplates("res/templates")

        parser_near_target = ClassicNearTargetsParser()
        parser_target = ClassicTargetParser(templates)
        handler_spoil_auto_farm = HandlerSpoilerAutoFarm(controller_spoil_auto_farm, parser_near_target, parser_target)

        super().__init__(win_cap, 1, [handler_spoil_auto_farm])


class C3ElmoreFarmApp(BaseApp):
    def __init__(self, char_name):
        super().__init__(WinCap(char_name), 1, [])
