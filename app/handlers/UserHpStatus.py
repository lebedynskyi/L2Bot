from app.handlers.BaseHandler import BaseHandler


class UserStatusHandler(BaseHandler):
    def __init__(self, status_parser):
        self.status_parser = status_parser

    def _on_tick(self, screen_rgb, current_time, last_action_delta):
        if last_action_delta > 10:
            hp = self.status_parser.parse_image(screen_rgb)
            if hp:
                self.write_log("Status", "player HP -> {}/{}".format(hp[0], hp[1]))
