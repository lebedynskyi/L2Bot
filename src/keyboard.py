import logging
import time

import pyautogui


class BaseKeyboard:
    KEY_MOUSE_LEFT = 1
    KEY_MOUSE_RIGHT = 2
    KEY_MOUSE_MIDDLE = 4

    def f1(self):
        pass

    def f2(self):
        pass

    def f3(self):
        pass

    def f4(self):
        pass

    def f5(self):
        pass

    def f6(self):
        pass

    def f7(self):
        pass

    def f8(self):
        pass

    def f9(self):
        pass

    def f10(self):
        pass

    def f11(self):
        pass

    def f12(self):
        pass

    def enter(self):
        pass

    def esc(self):
        pass

    def text(self, text):
        pass

    def mouse_move(self, x, y):
        pass

    def mouse_click(self, btn, cords):
        pass

    def mouse_down(self, btn):
        pass

    def mouse_up(self, btn):
        pass


class ArduinoKeyboard(BaseKeyboard):
    import serial
    arduino = None
    logger = logging.getLogger("ArduinoKeyboard")

    def __init__(self, port, baudrate=9600, time_out=0.01):
        self.logger.info("Arduino initialization", answer)
        self.arduino = self.serial.Serial(port=port, baudrate=baudrate, timeout=time_out)

        question = str.encode("Initialized")
        answer = self._arduino_write(question)

        self.logger.info("Arduino initialization answer -> '%s'", answer)
        if answer != question:
            raise ConnectionError("Not expected answer from arduino keyboard")

    def f1(self):
        data = str.encode("1{}".format(0xC2))
        answer = self._arduino_write(data)
        return data == answer

    def f2(self):
        data = str.encode("1{}".format(0xC3))
        answer = self._arduino_write(data)
        return data == answer

    def f3(self):
        data = str.encode("1{}".format(0xC4))
        answer = self._arduino_write(data)
        return data == answer

    def f4(self):
        data = str.encode("1{}".format(0xC5))
        answer = self._arduino_write(data)
        return data == answer

    def f5(self):
        data = str.encode("1{}".format(0xC6))
        answer = self._arduino_write(data)
        return data == answer

    def f6(self):
        data = str.encode("1{}".format(0xC7))
        answer = self._arduino_write(data)
        return data == answer

    def f7(self):
        data = str.encode("1{}".format(0xC8))
        answer = self._arduino_write(data)
        return data == answer

    def f8(self):
        data = str.encode("1{}".format(0xC9))
        answer = self._arduino_write(data)
        return data == answer

    def f9(self):
        data = str.encode("1{}".format(0xCA))
        answer = self._arduino_write(data)
        return data == answer

    def f10(self):
        data = str.encode("1{}".format(0xCB))
        answer = self._arduino_write(data)
        return data == answer

    def f11(self):
        data = str.encode("1{}".format(0xCC))
        answer = self._arduino_write(data)
        return data == answer

    def f12(self):
        data = str.encode("1{}".format(0xCD))
        answer = self._arduino_write(data)
        return data == answer

    def enter(self):
        data = str.encode("1{}".format(0xB0))
        answer = self._arduino_write(data)
        return data == answer

    def esc(self):
        data = str.encode("1{}".format(0xB1))
        answer = self._arduino_write(data)
        return data == answer

    def text(self, text):
        data = str.encode("2{}".format(text))
        answer = self._arduino_write(data)
        return data == answer

    def mouse_down(self, btn):
        data = str.encode("7{}".format(btn))
        answer = self._arduino_write(data)
        return data == answer

    def mouse_up(self, btn):
        data = str.encode("8{}".format(btn))
        answer = self._arduino_write(data)
        return data == answer

    def mouse_move(self, x, y):
        mouse_x, mouse_y = pyautogui.position()
        x_delta = int(mouse_x) - int(x)
        y_delta = int(mouse_y) - int(y)

        znak_x = "+" if x_delta < 0 else "-"
        znak_y = "+" if y_delta < 0 else "-"

        cords_value = abs(x_delta) * 0xFFFF + abs(y_delta)
        data = "5{}{}{}".format(znak_x, znak_y, cords_value)
        answer = self._arduino_write(data.encode())
        return data == answer

    def mouse_click(self, btn, cords=None):
        if cords is not None:
            self.mouse_move(cords[0], cords[1])
            time.sleep(0.2)

        data = str.encode("6{}".format(btn))
        answer = self._arduino_write(data)
        return data == answer

    def _arduino_write(self, data):
        self.arduino.write(data)
        time.sleep(0.1)
        answer = self.arduino.readline()
        return answer
