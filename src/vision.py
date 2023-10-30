from abc import ABC

from src.base import Capture
from src.parser.base import TargetParser, NearTargetsParser
from src.parser.classic import ClassicTargetParser, ClassicNearTargetsParser
from src.template import ClassicTemplates


class Vision(ABC):
    def __init__(self, capture: Capture):
        self.capture = capture

    def target(self):
        raise NotImplementedError("target() not implemented")

    def near_targets(self):
        raise NotImplementedError("near_targets() not implemented")


class ClassicVision(Vision):
    parser_target: TargetParser
    parser_near_targets: NearTargetsParser

    def __init__(self, capture: Capture, templates: ClassicTemplates):
        super().__init__(capture)
        self.parser_target = ClassicTargetParser(templates)
        self.parser_near_targets = ClassicNearTargetsParser(templates)

    def target(self):
        rgb, grey = self.capture.screenshot()
        return self.parser_target.parse(rgb, grey)

    def near_targets(self):
        rgb, grey = self.capture.screenshot()
        return self.parser_near_targets.parse(rgb, grey)
