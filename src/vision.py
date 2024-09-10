from abc import ABC

from src.base import Capture
from src.parser.c4 import ManorC4Parser
from src.parser.classic import ClassicTargetParser, ClassicNearTargetsParser, ClassicUserStatusParser
from src.parser.result import ManorWindowResult, ManorWindowPriceListResult, ManorWindowCropListResult
from src.template import ClassicTemplates, C4Templates


class Vision(ABC):
    def __init__(self, capture: Capture):
        self.capture = capture

    def target(self):
        raise NotImplementedError("target() is not implemented")

    def near_targets(self):
        raise NotImplementedError("near_targets() is not implemented")

    def user_status(self):
        raise NotImplementedError("user_status() is not implemented")

    def manor_window(self) -> ManorWindowResult:
        raise NotImplementedError("manor_window() is not implemented")

    def manor_crop_list(self) -> ManorWindowCropListResult:
        raise NotImplementedError("manor_window() is not implemented")

    def manor_price_list(self) -> ManorWindowPriceListResult:
        raise NotImplementedError("manor_price_list() is not implemented")

    def manor_price_list_chooser(self):
        raise NotImplementedError("manor_price_list_chooser() is not implemented")


class C4Vision(Vision):
    def __init__(self, capture: Capture, templates: C4Templates):
        super().__init__(capture)
        self.manor_parser = ManorC4Parser(templates)

    def manor_window(self):
        rgb, grey = self.capture.screenshot()
        return self.manor_parser.manor_window(grey)

    def manor_crop_list(self) -> ManorWindowCropListResult:
        rgb, grey = self.capture.screenshot()
        return self.manor_parser.crop_list(grey)

    def manor_price_list(self) -> ManorWindowPriceListResult:
        rgb, grey = self.capture.screenshot()
        return self.manor_parser.price_list(grey)

    def manor_price_list_chooser(self):
        rgb, grey = self.capture.screenshot()
        return self.manor_parser.price_list_chooser(grey)


class ClassicVision(Vision):
    def __init__(self, capture: Capture, templates: ClassicTemplates):
        super().__init__(capture)
        self.parser_target = ClassicTargetParser(templates)
        self.parser_status = ClassicUserStatusParser(templates)
        self.parser_near_targets = ClassicNearTargetsParser()

    def target(self):
        rgb, grey = self.capture.screenshot()
        return self.parser_target.parse(rgb, grey)

    def near_targets(self):
        rgb, grey = self.capture.screenshot()
        return self.parser_near_targets.parse(rgb, grey)

    def user_status(self):
        rgb, grey = self.capture.screenshot()
        return self.parser_status.parse(rgb, grey)
