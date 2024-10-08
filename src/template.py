import logging
import os

import cv2

logger = logging.getLogger("Template")

"""
Templates are class holder of grey scaled images. Base template class contain base templates for all chronicles.
If you need to add server / chronicles specific templates - just make child class and add your own
"""


class Template:
    ui_dialog = None
    ui_target = None
    ui_fishing_dialog = None

    user_death = None
    user_status = None
    user_pet = None

    manor_window = None
    manor_crop_list = None
    manor_price_list = None
    manor_price_list_chooser = None

    def __init__(self, res_folder, sub_folder):
        stub = self._read_template(res_folder, sub_folder, "stub.png")

        if stub is None:
            logger.warning("No stub found in res folder %s/%s", res_folder, sub_folder)
            exit(1)

        self.ui_fishing_dialog = self._read_template(res_folder, sub_folder, "dialog_fishing.png")
        self.ui_target = self._read_template(res_folder, sub_folder, "target.png")
        self.user_status = self._read_template(res_folder, sub_folder, "user_status.png")
        self.manor_window = self._read_template(res_folder, sub_folder, "manor_window.png")
        self.manor_crop_list = self._read_template(res_folder, sub_folder, "manor_crop_list.png")
        self.manor_price_list = self._read_template(res_folder, sub_folder, "manor_price_list.png")

    @staticmethod
    def _read_template(res_folder, sub_folder, name):
        template_file = os.path.join(res_folder, sub_folder, name)
        if os.path.exists(template_file):
            return cv2.imread(template_file, flags=cv2.IMREAD_GRAYSCALE)


class GraciaRebornTemplates(Template):
    def __init__(self, folder):
        super().__init__(folder, "gracia")
        self.captcha_dualbox = None
        self.captcha_solo = None


class C3Templates(Template):
    def __init__(self, folder):
        super().__init__(folder, "c3")


class C4Templates(Template):
    def __init__(self, folder):
        super().__init__(folder, "c4")


class ClassicTemplates(Template):
    def __init__(self, folder):
        super().__init__(folder, "classic")
