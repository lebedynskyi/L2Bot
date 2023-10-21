import logging
from abc import ABC, abstractmethod


class BaseKeyboard(ABC):
    @abstractmethod
    def f1(self):
        pass

    @abstractmethod
    def f2(self):
        pass

    @abstractmethod
    def f3(self):
        pass

    @abstractmethod
    def f4(self):
        pass

    @abstractmethod
    def f5(self):
        pass

    @abstractmethod
    def f6(self):
        pass

    @abstractmethod
    def f7(self):
        pass

    @abstractmethod
    def f8(self):
        pass

    @abstractmethod
    def f9(self):
        pass

    @abstractmethod
    def f10(self):
        pass

    @abstractmethod
    def f11(self):
        pass

    @abstractmethod
    def f12(self):
        pass

    @abstractmethod
    def enter(self):
        pass

    @abstractmethod
    def esc(self):
        pass

    @abstractmethod
    def text(self, text):
        pass

    @abstractmethod
    def mouse_move(self, x, y):
        pass

    @abstractmethod
    def mouse_click(self, btn, cords):
        pass

    @abstractmethod
    def mouse_down(self, btn):
        pass

    @abstractmethod
    def mouse_up(self, btn):
        pass


class ArduinoKeyboard(BaseKeyboard):
    import serial
    arduino = None
    logger = logging.getLogger("ArduinoKeyboard")

    def __init__(self, port, baudrate=9600, time_out=0.01):
        question = str.encode("Initialization")

        self.arduino = self.serial.Serial(port=port, baudrate=baudrate, timeout=time_out)
        self.arduino.write(question)
        answer = self.arduino.readline()

        self.logger.info("Arduino initialization answer -> %s",  answer)
        if answer != question:
            raise ConnectionError("Not expected answer from arduino keyboard")

    def f1(self):
        data = str.encode("1{}".format(0xC2))
        self.arduino.write(data)
        answer = self.arduino.readline()
        return data == answer

    def f2(self):
        data = str.encode("1{}".format(0xC3))
        self.arduino.write(data)
        answer = self.arduino.readline()
        return data == answer

    def f3(self):
        data = str.encode("1{}".format(0xC4))
        self.arduino.write(data)
        answer = self.arduino.readline()
        return data == answer

    def f4(self):
        data = str.encode("1{}".format(0xC5))
        self.arduino.write(data)
        answer = self.arduino.readline()
        return data == answer

    def f5(self):
        data = str.encode("1{}".format(0xC6))
        self.arduino.write(data)
        answer = self.arduino.readline()
        return data == answer

    def f6(self):
        data = str.encode("1{}".format(0xC7))
        self.arduino.write(data)
        answer = self.arduino.readline()
        return data == answer

    def f7(self):
        data = str.encode("1{}".format(0xC8))
        self.arduino.write(data)
        answer = self.arduino.readline()
        return data == answer

    def f8(self):
        data = str.encode("1{}".format(0xC9))
        self.arduino.write(data)
        answer = self.arduino.readline()
        return data == answer

    def f9(self):
        data = str.encode("1{}".format(0xCA))
        self.arduino.write(data)
        answer = self.arduino.readline()
        return data == answer

    def f10(self):
        data = str.encode("1{}".format(0xCB))
        self.arduino.write(data)
        answer = self.arduino.readline()
        return data == answer

    def f11(self):
        data = str.encode("1{}".format(0xCC))
        self.arduino.write(data)
        answer = self.arduino.readline()
        return data == answer

    def f12(self):
        data = str.encode("1{}".format(0xCD))
        self.arduino.write(data)
        answer = self.arduino.readline()
        return data == answer

    def enter(self):
        data = str.encode("1{}".format(0xB0))
        self.arduino.write(data)
        answer = self.arduino.readline()
        return data == answer

    def esc(self):
        data = str.encode("1{}".format(0xB1))
        self.arduino.write(data)
        answer = self.arduino.readline()
        return data == answer

    def text(self, text):
        data = str.encode("2{}".format(text))
        self.arduino.write(data)
        answer = self.arduino.readline()
        return data == answer

    def mouse_move(self, x, y):
        mouse_x, mouse_y = pyautogui.position()
        x_delta = int(mouse_x) - int(x)
        y_delta = int(mouse_y) - int(y)

        znak_x = "+" if x_delta < 0 else "-"
        znak_y = "+" if y_delta < 0 else "-"

        cords_value = abs(x_delta) * 0xFFFF + abs(y_delta)
        data = "5{}{}{}".format(znak_x, znak_y, cords_value)
        self.arduino.write(data.encode())
        answer = self.arduino.readline()
        return data == answer

    def mouse_click(self, btn, cords=None):
        if cords is not None:
            self.mouse_move(cords[0], cords[1])

        data = str.encode("6{}".format(btn))
        self.arduino.write(data)
        answer = self.arduino.readline()
        return data == answer

    def mouse_down(self, btn):
        data = str.encode("7{}".format(btn))
        self.arduino.write(data)
        answer = self.arduino.readline()
        return data == answer

    def mouse_up(self, btn):
        data = str.encode("8{}".format(btn))
        self.arduino.write(data)
        answer = self.arduino.readline()
        return data == answer