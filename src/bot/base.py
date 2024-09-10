from abc import ABC

from src.keyboard import BaseKeyboard


class BaseController(ABC):
    def __init__(self, keyboard: BaseKeyboard):
        self.keyboard = keyboard


class BehaviourHandler:
    is_paused = False

    last_action_time = 0
    next_action_time = 0

    def on_tick(self, time):
        if not self.is_paused:
            if time >= self.next_action_time:
                time_shift = self._on_tick(time - self.last_action_time)
                self.last_action_time = time

                if time_shift is not None:
                    self.next_action_time = time + time_shift

    def _on_tick(self, delta):
        return None
