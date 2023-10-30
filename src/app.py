from src.bot.bufs import HandlerUseBottles, ControllerUseBottles
from src.bot.spoiler import ControllerSpoilerAutoFarm, HandlerSpoilerAutoFarm
from src.keyboard import ArduinoKeyboard
from src.template import ClassicTemplates
from src.vision import ClassicVision


def farm_app():
    from src.win_capture import WinCap
    win_cap = WinCap("Tui")
    keyboard = ArduinoKeyboard(port="COM3")
    controller = ControllerSpoilerAutoFarm(keyboard, win_cap)
    templates = ClassicTemplates("res/templates")
    vision = ClassicVision(win_cap, templates)

    return (
        HandlerSpoilerAutoFarm(controller, vision, mobs=(
            {"name": "Hobgoblin", "is_aggr": False},
        )),
        HandlerUseBottles(ControllerUseBottles(keyboard))
    )


def manor_app():
    return ()


def mock_app():
    pass
