import cv2


def load_templates(folder):
    return Templates(Farm(
        target=cv2.imread("{folder}/farm/target_template.png".format(folder=folder))
    ), Manor(

    ), Status(

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
    pass


class Captcha:
    def __init__(self, warn_dialog):
        self.warn_dialog = warn_dialog
