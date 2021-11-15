from abc import ABC, abstractmethod


class Keyboard(ABC):
    KEY_F1 = None
    KEY_F2 = None
    KEY_F3 = None
    KEY_F4 = None
    KEY_F5 = None
    KEY_F6 = None
    KEY_F7 = None
    KEY_F8 = None
    KEY_F9 = None
    KEY_F10 = None
    KEY_F11 = None
    KEY_F12 = None
    KEY_ENTER = None
    KEY_ESC = None

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
    def mouse_down(self):
        pass

    @abstractmethod
    def mouse_up(self):
        pass

    @abstractmethod
    def mouse_click(self):
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

        self.KEY_ENTER = 0xCD
        self.KEY_ESC = 0xCD

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

    def mouse_move(self, x_range, y_range):
        pass

    def mouse_click(self):
        pass

    def mouse_down(self):
        pass

    def mouse_up(self):
        pass

    def close(self):
        self.arduino.close()
        self.arduino = None


class SoftwareKeyboard(Keyboard):
    import pyautogui

    def init(self):
        self.pyautogui.FAILSAFE = False
        self.pyautogui.PAUSE = 0.02

    def press(self, value):
        pass

    def text(self, text):
        pass

    def mouse_move(self, x_range, y_range):
        pass

    def mouse_click(self):
        pass

    def mouse_down(self):
        pass

    def mouse_up(self):
        pass


if __name__ == '__main__':
    keyboard = ArduinoKeyboard()
    keyboard.init()

    try:
        while True:
            inp = input("Enter a value: ")
            print("Sending -> {}".format(inp))
            res = keyboard.text(inp)
            print("Received -> {}".format(res))
    except Exception as e:
        keyboard.close()
