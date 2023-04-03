import cv2


def load_templates(folder):
    return Templates(Farm(
        target=cv2.imread("{folder}/farm/target_template.png".format(folder=folder))),
        Manor(
            manor_dialog_template=cv2.imread("{folder}/manor/manor_dialog_template.png".format(folder=folder)),
            crop_sales_dialog=cv2.imread("{folder}/manor/crop_sales_dialog.png".format(folder=folder)),
            chooser_template=cv2.imread("{folder}/manor/chooser_template.png".format(folder=folder)),
            chooser_expanded_template=cv2.imread("{folder}/manor/chooser_expanded_template.png".format(folder=folder))
        ), Status(
            user_death=cv2.imread("{folder}/status/user_death_template.png".format(folder=folder)),
            user_status=cv2.imread("{folder}/status/user_status_template.png".format(folder=folder)),
            user_pet=cv2.imread("{folder}/status/user_pet_template.png".format(folder=folder))
        ), Captcha(
            warn_dialog=cv2.imread("{folder}/captcha/warning_template.png".format(folder=folder)),
            dualbox_dialog=cv2.imread("{folder}/captcha/dualbox_template.png".format(folder=folder)),
            captcha_quiz_start=cv2.imread("{folder}/captcha/captcha_quiz_start.jpg".format(folder=folder)),
            captcha_quiz_continue=cv2.imread("{folder}/captcha/captcha_quiz_continue.jpg".format(folder=folder))
        ))


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
    def __init__(self, manor_dialog_template, crop_sales_dialog, chooser_template, chooser_expanded_template):
        self.chooser_expanded_template = chooser_expanded_template
        self.chooser_template = chooser_template
        self.crop_sales_dialog = crop_sales_dialog
        self.manor_dialog_template = manor_dialog_template


class Status:
    def __init__(self, user_death, user_status, user_pet):
        self.user_pet = user_pet
        self.user_status = user_status
        self.user_death = user_death


class Captcha:
    def __init__(self, warn_dialog, dualbox_dialog, captcha_quiz_start, captcha_quiz_continue):
        self.captcha_quiz_continue = captcha_quiz_continue
        self.captcha_quiz_start = captcha_quiz_start
        self.dualbox_dialog = dualbox_dialog
        self.warn_dialog = warn_dialog
