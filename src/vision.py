from abc import ABC

from src.base import Capture
from src.parser.classic import ClassicTargetParser, ClassicNearTargetsParser, ClassicUserStatusParser
from src.template import ClassicTemplates


class Vision(ABC):
    def __init__(self, capture: Capture):
        self.capture = capture

    def target(self):
        raise NotImplementedError("target() is not implemented")

    def near_targets(self):
        raise NotImplementedError("near_targets() is not implemented")

    def user_status(self):
        raise NotImplementedError("user_status() is not implemented")


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

