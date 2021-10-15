import numpy as np

from app.handlers.BaseHandler import BaseHandler


class UserTeleportedHandler(BaseHandler):
    def __init__(self, color_parser):
        self.color_parser = color_parser

    def _on_tick(self, screen_rgb, current_time, last_action_delta):
        x, y = screen_rgb.shape[0], screen_rgb.shape[1]
        center = int(y / 2), int(x / 2)
        point1 = int(center[0] + center[0] / 2), int(center[1] + center[1] / 2)
        point2 = int(center[0] + center[0] / 2), int(center[1] - center[1] / 2)

        colors = self.color_parser.parse_image(screen_rgb, points=[point1, point2])

        dark_colors = []

        for c in colors:
            if c[0] < 10 and c[1] < 10 and c[2] < 10:
                # The point is dark!
                dark_colors.append(True)
            else:
                break
        else:
            self.write_log("Teleport", "Detected teleporting. Write some word to chat !")
