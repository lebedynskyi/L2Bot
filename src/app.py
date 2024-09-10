from src.bot.bufs import HandlerUseBottles, ControllerUseBottles
from src.bot.manor import ManorSellerBehaviour
from src.bot.spoiler import ControllerSpoilerAutoFarm, HandlerSpoilerAutoFarm
from src.keyboard import ArduinoKeyboard, SoftwareKeyboard
from src.template import ClassicTemplates, C4Templates
from src.vision import ClassicVision, C4Vision


def farm_app(window_name):
    from src.win_capture import WinCap
    win_cap = WinCap(window_name)
    keyboard = ArduinoKeyboard(port="COM3")
    controller = ControllerSpoilerAutoFarm(keyboard, win_cap)
    templates = ClassicTemplates("res/templates")
    vision = ClassicVision(win_cap, templates)

    return (
        HandlerSpoilerAutoFarm(controller, vision, mobs=(
            {"name": "Grave robber ranger", "is_aggr": False},
            {"name": " Grave robber lookout", "is_aggr": False},
            {"name": "Grave robber guard", "is_aggr": True},
            # {"name": "Hobgoblin", "is_aggr": False},

            # {"name": "Gamstone beast", "is_aggr": False},
            # {"name": "Mineshaft Bat", "is_aggr": False},
            # {"name": "Monster Eye Tracker", "is_aggr": False},
            # {"name": "Akaste Bone Soldier", "is_aggr": True},
            # {"name": "Darkstone Golem", "is_aggr": False},
        )),
        # HandlerUseBottles(ControllerUseBottles(keyboard))
    )


def manor_app(window_name):
    from src.win_capture import WinCap
    win_cap = WinCap(window_name)
    keyboard = SoftwareKeyboard()
    return (
        ManorSellerBehaviour(
            keyboard,
            C4Vision(win_cap, C4Templates("f:\\Projects\\Python\\antbl2\\res\\templates")),
            castle_index=2),
    )
