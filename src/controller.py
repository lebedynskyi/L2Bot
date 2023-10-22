from abc import ABC

from src.keyboard import BaseKeyboard


class BaseController(ABC):
    def __init__(self, keyboard: BaseKeyboard):
        self.keyboard = keyboard
