import time
from abc import ABC, abstractmethod
import pyautogui

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.02


class Keyboard(ABC):
    @abstractmethod
    def init(self, time_out):
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
    def mouse_click(self, btn, cords):
        pass


class MockKeyboard(Keyboard):
    def __init__(self):
        self.KEY_F1 = None
        self.KEY_F2 = None
        self.KEY_F3 = None
        self.KEY_F4 = None
        self.KEY_F5 = None
        self.KEY_F6 = None
        self.KEY_F7 = None
        self.KEY_F8 = None
        self.KEY_F9 = None
        self.KEY_F10 = None
        self.KEY_F11 = None
        self.KEY_F12 = None
        self.KEY_ENTER = None
        self.KEY_ESC = None

        self.KEY_MOUSE_LEFT = None
        self.KEY_MOUSE_RIGHT = None
        self.KEY_MOUSE_MIDDLE = None

    def init(self, time_out):
        pass

    def press(self, value):
        pass

    def text(self, text):
        pass

    def mouse_move(self, x_range, y_range):
        pass

    def mouse_down(self, btn):
        pass

    def mouse_up(self, btn):
        pass

    def mouse_click(self, btn, cords):
        pass


class SoftKeyboard(Keyboard):
    def init(self, time_out):
        pass

    def press(self, value):
        pyautogui.press(value)

    def text(self, text):
        pyautogui.typewrite(text)

    def mouse_move(self, x, y):
        pyautogui.moveTo(x, y, duration=0.2)

    def mouse_down(self, btn):
        pyautogui.mouseDown()

    def mouse_up(self, btn):
        pyautogui.mouseUp()

    def mouse_click(self, btn):
        if btn == self.KEY_MOUSE_LEFT:
            pyautogui.leftClick()
        elif btn == self.KEY_MOUSE_RIGHT:
            pyautogui.rightClick()
        elif btn == self.KEY_MOUSE_MIDDLE:
            pyautogui.middleClick()

    def __init__(self):
        self.KEY_F1 = "F1"
        self.KEY_F2 = "F2"
        self.KEY_F3 = "F3"
        self.KEY_F4 = "F4"
        self.KEY_F5 = "F5"
        self.KEY_F6 = "F6"
        self.KEY_F7 = "F7"
        self.KEY_F8 = "F8"
        self.KEY_F9 = "F9"
        self.KEY_F10 = "F10"
        self.KEY_F11 = "F11"
        self.KEY_F12 = "F12"
        self.KEY_ENTER = "ENTER"
        self.KEY_ESC = "ESC"

        self.KEY_MOUSE_LEFT = 1
        self.KEY_MOUSE_RIGHT = 2
        self.KEY_MOUSE_MIDDLE = 4


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

    def init(self, time_out):
        question = str.encode("Initialized")

        self.arduino = self.serial.Serial(port=self.port, baudrate=self.baudrate, timeout=time_out)
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

    def close(self):
        self.arduino.close()
        self.arduino = None


if __name__ == '__main__':
    keyboard = SoftKeyboard()
    keyboard.init()

    keyboard.mouse_move(700, 850)
    time.sleep(1)
    keyboard.mouse_click(keyboard.KEY_MOUSE_LEFT)
    keyboard.text("Hello world")
    keyboard.press(keyboard.KEY_ENTER)
