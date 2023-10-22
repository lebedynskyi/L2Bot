import logging

from abc import ABC, abstractmethod

logger = logging.getLogger("Handler")

STATE_IDLE = 0


class BaseHandler(ABC):
    last_action_time = 0
    is_paused = False
    state = STATE_IDLE

    def on_tick(self, screen_rgb, screen_gray, time):
        logger.debug("On tick. time %s", time)
        if not self.is_paused:
            delta = time - self.last_action_time

            if self._on_tick(screen_rgb, screen_gray, time, delta):
                self.last_action_time = time

    @abstractmethod
    def _on_tick(self, screen_rgb, screen_gray, time, delta):
        pass
