import logging

from abc import ABC, abstractmethod

logger = logging.getLogger("Handler")


class BaseHandler(ABC):
    last_action_time = 0
    is_paused = False

    def on_tick(self, screen_rgb, screen_grey, time):
        logger.debug("On tick. time %s", time)
        if not self.is_paused:
            last_action_delta = time - self.last_action_time

            if self._on_tick(screen_rgb, screen_grey, time, last_action_delta):
                self.last_action_time = time

    @abstractmethod
    def _on_tick(self, screen_rgb, screen_grey, time, delta):
        pass
