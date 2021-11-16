import cv2


def load_templates(folder):
    return Templates(Farm(
        target=cv2.imread("{folder}/farm/target_template.png".format(folder=folder))
    ), Manor(

    ), Status(
        user_death=cv2.imread("{folder}/status/user_death_template.png".format(folder=folder))
    ), Captcha(
        warn_dialog=cv2.imread("{folder}/captcha/warning_template.png".format(folder=folder))
    ))


class TemplateLoader:
    pass


class Templates:
    def __init__(self, farm, manor, status, captcha):
        self.captcha = captcha
        self.status = status
        self.manor = manor
        self.farm = farm


class Farm:
    def __init__(self, target):
        self.target = target


class Manor:
    pass


class Status:
    def __init__(self, user_death):
        self.user_death = user_death


class Captcha:
    def __init__(self, warn_dialog):
        self.warn_dialog = warn_dialog
