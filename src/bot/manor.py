import logging
import time

from src.bot.base import BehaviourHandler
from src.keyboard import BaseKeyboard
from src.vision import Vision


class ManorSellerBehaviour(BehaviourHandler):
    logger = logging.getLogger("ManorSellerController")

    STATE_WINDOW = 1
    STATE_CROP_LIST = 2
    STATE_PRICE_LIST = 3
    STATE_PRICE_LIST_CHOOSER = 4
    STATE_PRICE_LIST_MAX_PRICE = 5
    STATE_PRICE_LIST_OK = 6
    STATE_WINDOW_SELL = 7

    state = STATE_WINDOW

    result_window = None
    result_window_crop_list = None
    result_price_list = None
    result_price_list_chooser = None

    def __init__(self, keyboard: BaseKeyboard, vision: Vision, crop_index=1, castle_index=1):
        super().__init__()
        self.castle_index = castle_index
        self.crop_index = crop_index
        self.vision = vision
        self.keyboard = keyboard

    def _on_tick(self, delta):
        if self.state == self.STATE_WINDOW:
            return self._handle_state_window()
        if self.state == self.STATE_CROP_LIST:
            return self._handle_state_crop_list()
        if self.state == self.STATE_PRICE_LIST:
            return self._handle_state_price_list()
        if self.state == self.STATE_PRICE_LIST_CHOOSER:
            return self._handle_price_list_chooser()
        if self.state == self.STATE_PRICE_LIST_MAX_PRICE:
            return self._handle_price_list_max_price()
        if self.state == self.STATE_PRICE_LIST_OK:
            return self._handle_price_list_ok()
        if self.state == self.STATE_WINDOW_SELL:
            return self._handle_window_sell()

    def reset(self):
        self.state = self.STATE_WINDOW
        self.result_window = None
        self.result_price_list = None
        self.result_price_list_chooser = None

    def _handle_state_window(self):
        self.result_window = self.vision.manor_window()
        if self.result_window.exist:
            self.logger.debug("Found manor window")
            sell_btn_cords = self.result_window.sell_crop_btn.middle()
            self.keyboard.mouse_click(None, (
                sell_btn_cords[0] + self.vision.capture.offset_x,
                sell_btn_cords[1] + self.vision.capture.offset_y)
                                      )
            self.state = self.STATE_CROP_LIST

    def _handle_state_crop_list(self):
        self.result_window_crop_list = self.vision.manor_crop_list()
        if self.result_window_crop_list.exist:
            if self.crop_index == 1:
                crop_btn = self.result_window_crop_list.first_crop_item.middle()
            elif self.crop_index == 2:
                crop_btn = self.result_window_crop_list.second_crop_item.middle()
            else:
                crop_btn = self.result_window_crop_list.first_crop_item.middle()

            self.logger.debug("Found Crop list")

            self.keyboard.mouse_click(
                None, (
                    crop_btn[0] + self.vision.capture.offset_x,
                    crop_btn[1] + self.vision.capture.offset_y)
            )

            time.sleep(0.1)
            self.keyboard.mouse_click(None, None)
            self.state = self.STATE_PRICE_LIST

    def _handle_state_price_list(self):
        self.result_price_list = self.vision.manor_price_list()
        if self.result_price_list.exist:
            self.logger.debug("Found price list")
            chooser_btn = self.result_price_list.chooser_btn.middle()

            self.keyboard.mouse_click(
                None, (
                    chooser_btn[0] + self.vision.capture.offset_x,
                    chooser_btn[1] + self.vision.capture.offset_y)
            )
            self.state = self.STATE_PRICE_LIST_CHOOSER
            return 0.1

    def _handle_price_list_chooser(self):
        self.logger.debug("price list chooser")
        if self.castle_index == 1:
            castle_btn = self.result_price_list.first_crop_item.middle()
        elif self.castle_index == 2:
            castle_btn = self.result_price_list.second_crop_item.middle()
        elif self.castle_index == 3:
            castle_btn = self.result_price_list.third_crop_item.middle()
        elif self.castle_index == 4:
            castle_btn = self.result_price_list.fourth_crop_item.middle()
        else:
            castle_btn = self.result_price_list.first_crop_item.middle()

        self.keyboard.mouse_click(
            None, (
                castle_btn[0] + self.vision.capture.offset_x,
                castle_btn[1] + self.vision.capture.offset_y)
        )

        self.state = self.STATE_PRICE_LIST_MAX_PRICE

    def _handle_price_list_max_price(self):
        self.logger.debug("price list max price")
        max_price_btn = self.result_price_list.max_price_btn.middle()
        self.keyboard.mouse_click(
            None, (
                max_price_btn[0] + self.vision.capture.offset_x,
                max_price_btn[1] + self.vision.capture.offset_y)
        )
        self.state = self.STATE_PRICE_LIST_OK

    def _handle_price_list_ok(self):
        self.logger.debug("price list ok")
        ok_btn = self.result_price_list.ok_btn.middle()
        self.keyboard.mouse_click(
            None, (
                ok_btn[0] + self.vision.capture.offset_x,
                ok_btn[1] + self.vision.capture.offset_y)
        )
        self.state = self.STATE_WINDOW_SELL

    def _handle_window_sell(self):
        self.logger.debug("window sell")
        ok_btn = self.result_window_crop_list.sell_crop_btn.middle()
        self.keyboard.mouse_move(
            ok_btn[0] + self.vision.capture.offset_x,
            ok_btn[1] + self.vision.capture.offset_y
        )
        self.state = -1
