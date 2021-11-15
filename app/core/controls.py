from abc import ABC, abstractmethod
import pyautogui

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.02


class Keyboard(ABC):
    @abstractmethod
    def init(self):
        pass

    @abstractmethod
    def press(self, value):
        pass

    @abstractmethod
    def text(self, text):
        pass

    @abstractmethod
    def mouse_move(self, x_range, y_range):
        pass

    @abstractmethod
    def mouse_down(self, btn):
        pass

    @abstractmethod
    def mouse_up(self, btn):
        pass

    @abstractmethod
    def mouse_click(self, btn):
        pass


class ArduinoKeyboard(Keyboard):
    import serial
    arduino = None

    def __init__(self, port='COM5', baudrate=9600):
        self.KEY_F1 = 0xC2
        self.KEY_F2 = 0xC3
        self.KEY_F3 = 0xC4
        self.KEY_F4 = 0xC5
        self.KEY_F5 = 0xC6
        self.KEY_F6 = 0xC7
        self.KEY_F7 = 0xC8
        self.KEY_F8 = 0xC9
        self.KEY_F9 = 0xCA
        self.KEY_F10 = 0xCB
        self.KEY_F11 = 0xCC
        self.KEY_F12 = 0xCD
        self.KEY_ENTER = 0xB0
        self.KEY_ESC = 0xB1

        self.KEY_MOUSE_LEFT = 1
        self.KEY_MOUSE_RIGHT = 2
        self.KEY_MOUSE_MIDDLE = 4

        self.baudrate = baudrate
        self.port = port

    def init(self):
        question = str.encode("Initialized")

        self.arduino = self.serial.Serial(port=self.port, baudrate=self.baudrate, timeout=0.1)
        self.arduino.write(question)
        answer = self.arduino.readline()

        print("Arduino initialization answer -> {}".format(answer))
        if answer != question:
            raise ConnectionError("Not expected answer from arduino")

    def press(self, value):
        data = str.encode("1{}".format(value))
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
        x_delta, y_delta = mouse_x - x, mouse_y - y

        znak_x = "+" if x_delta < 0 else "-"
        znak_y = "+" if y_delta < 0 else "-"

        data = "5{}{}{}".format(znak_x, znak_y, abs(x_delta) * 0xFFFF + abs(y_delta))
        self.arduino.write(data.encode())
        answer = self.arduino.readline()
        return data == answer

    def mouse_click(self, btn):
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

    def close(self):
        self.arduino.close()
        self.arduino = None


if __name__ == '__main__':
    keyboard = ArduinoKeyboard()
    keyboard.init()
