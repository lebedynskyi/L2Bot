from abc import ABC

from app.keyboard import BaseKeyboard


class BaseController(ABC):
    def __init__(self, keyboard: BaseKeyboard):
        self.keyboard = keyboard
