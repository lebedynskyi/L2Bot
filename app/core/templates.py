import cv2


def load_templates(folder):
    return Templates(Farm(
        target=cv2.imread("{folder}/farm/target_template.png".format(folder=folder))
    ), Manor(

    ), Status(

    ))


class TemplateLoader:
    pass


class Templates:
    def __init__(self, farm, manor, status):
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
    pass
