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
        self.write_log("Teleport", colors)
