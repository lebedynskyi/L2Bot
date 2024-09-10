from src.parser.base import ManorParser
from src.template import C4Templates


class ManorC4Parser(ManorParser):
    window_sell_btn_x_offset = 512
    window_sell_btn_y_offset = 206
    windows_sell_btn_h = 20
    windows_sell_btn_w = 70

    list_sell_btn_x_offset = 432
    list_sell_btn_y_offset = 224
    list_sell_btn_h = 20
    list_sell_btn_w = 70

    list_crop_item_y_offset = 18
    price_crop_item_y_offset = 18
    price_crop_item_x_offset = -110

    price_chooser_x_offset = 236
    price_chooser_y_offset = 125
    price_chooser_h = 16
    price_chooser_w = 16

    price_max_x_offset = 187
    price_max_y_offset = 147
    price_max_h = 20
    price_max_w = 65

    price_ok_x_offset = 85
    price_ok_y_offset = 185
    price_ok_h = 20
    price_ok_w = 70

    def __init__(self, templates: C4Templates, debug=False):
        super().__init__(templates, debug)
