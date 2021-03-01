class Data:
    def __init__(self, g_data, u_data):
        self.game_data = g_data
        self.user_data = u_data


class GameData:
    is_captcha = False
    captcha_text = ""


class PlayerData:
    hp = -1
    mp = -1
    cp = -1
