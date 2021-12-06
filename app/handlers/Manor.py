from datetime import datetime

import time

from app.handlers.BaseHandler import BaseHandler

STATE_MANOR_DIALOG = 0
STATE_CROP_CHOOSER = 1
STATE_CASTLES_LIST = 2
STATE_CASTLES_CHOOSER = 3
STATE_MAX_PRICE = 4
STATE_MAX_PRICE_OK = 5
STATE_SELL = 6
STATE_FINISH = 7

"""
General flow of manor handlers:

STATE_MANOR_DIALOG -> This is general manor window. Here we need to press sell crop btn to go list of crops
STATE_CROP_CHOOSER -> This is a window with list of available crops that player holds
STATE_CASTLES_LIST -> This is a window with list of castles that are ready to buy chosen crop
STATE_CASTLES_CHOOSER -> Same STATE_CASTLES_LIST but with opened drop down window
STATE_MAX_PRICE -> It mean use max number of crops that castle can receive
STATE_MAX_PRICE_OK -> We need to confirm chosen castle with chosen amount of crops by pressing ok button 
STATE_SELL -> Sell all crops. This button is in first dialog that can be found in STATE_MANOR_DIALOG
STATE_FINISH -> Just finish state to exit from the app

"""


class ManorSellCastle:
    def __init__(self, castle_name, alt_castle_name, start_index, finish_index=8, crop_number=1, castle_number=0):
        self.castle_number = castle_number
        self.castle_name = castle_name
        self.alternative_castle_name = alt_castle_name
        self.start_index = start_index
        self.finish_index = finish_index
        self.crop_number = crop_number


class ManorHandler(BaseHandler):
    current_state = STATE_MANOR_DIALOG
    start_time = 0
    finish_time = 0
    current_castle_index = 0

    cached_sell_btn = None
    cached_max_price_btn = None
    cached_ok_btn = None

    def __init__(self, keyboard, castles,
                 manor_dialog_parser, crop_list_parser, castles_list_parser, castles_chooser_parser):
        super().__init__(keyboard)
        self.castles = castles
        self.castles_list_chooser_parser = castles_chooser_parser
        self.castles_list_parser = castles_list_parser
        self.crop_list_parser = crop_list_parser
        self.manor_dialog_parser = manor_dialog_parser

    def _on_tick(self, screen_rgb, current_time, last_action_delta):
        move_click_btn = self.handle_state(screen_rgb)

        if move_click_btn is not None:
            # Just need some delay to let game handle mouse movement
            # self.keyboard.mouse_move(move_click_btn[0], move_click_btn[1])
            self.keyboard.mouse_click(self.keyboard.KEY_MOUSE_LEFT, move_click_btn)

            if self.current_state == STATE_CASTLES_LIST:
                # Double click for crop list chooser
                time.sleep(0.1)
                self.key    board.mouse_click(self.keyboard.KEY_MOUSE_LEFT, None)

        elif self.current_state == STATE_CROP_CHOOSER:
            # Manor is in maintenance mode. There is no chooser dialog
            time.sleep(0.1)
            self.start_time = datetime.now()
            self.keyboard.mouse_click(self.keyboard.KEY_MOUSE_LEFT, None)

    def handle_state(self, screen_rgb):
        if STATE_MANOR_DIALOG == self.current_state:
            self.start_time = datetime.now()
            sell_crop_btn = self.manor_dialog_parser.parse_image(screen_rgb)
            self.current_state = STATE_CROP_CHOOSER
            return sell_crop_btn

        if STATE_CROP_CHOOSER == self.current_state:
            chosen_crop, self.cached_sell_btn = self.crop_list_parser.parse_image(screen_rgb)

            if chosen_crop:
                self.current_state = STATE_CASTLES_LIST
            else:
                self.write_log("Manor", "No crops chooser dialog yet. Wait it")

            return chosen_crop

        if STATE_CASTLES_LIST == self.current_state:
            castles_drop_down_btn, self.cached_max_price_btn, self.cached_ok_btn = self.castles_list_parser.parse_image(
                screen_rgb)
            if castles_drop_down_btn:
                self.current_state = STATE_CASTLES_CHOOSER
            else:
                self.write_log("Manor", "No castles list dialog yet. Wait it")

            return castles_drop_down_btn

        if STATE_CASTLES_CHOOSER == self.current_state:
            castle_btn = self.castles_list_chooser_parser.parse_image(screen_rgb,
                                                                      castle=self.castles[self.current_castle_index])
            if castle_btn:
                self.current_state = STATE_MAX_PRICE
            else:
                self.write_log("Manor", "No interested castle found. Stop it?")
                exit(1)
            return castle_btn

        if STATE_MAX_PRICE == self.current_state:
            self.current_state = STATE_MAX_PRICE_OK
            return self.cached_max_price_btn

        if STATE_MAX_PRICE_OK == self.current_state:
            self.current_state = STATE_SELL
            return self.cached_ok_btn

        if STATE_SELL == self.current_state:
            self.finish_time = datetime.now()
            next_index = self.current_castle_index + 1
            if next_index < len(self.castles):
                self.current_castle_index = next_index
                self.current_state = STATE_MANOR_DIALOG
            else:
                self.current_state = STATE_FINISH

            self.write_log("Manor", "Sold crops")
            self.write_log("Manor", "Start time {}".format(self.start_time))
            self.write_log("Manor", "Finish time {}".format(self.finish_time))
            return self.cached_sell_btn

        if STATE_FINISH == self.current_state:
            exit(0)
