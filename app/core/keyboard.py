import serial

KEY_F1 = 0xC2
KEY_F2 = 0xC3
KEY_F3 = 0xC4
KEY_F4 = 0xC5
KEY_F5 = 0xC6
KEY_F6 = 0xC7
KEY_F7 = 0xC8
KEY_F8 = 0xC9
KEY_F9 = 0xCA
KEY_F10 = 0xCB
KEY_F11 = 0xCC
KEY_F12 = 0xCD


class ArduinoKeyboard:
    arduino = None

    def __init__(self, port='COM5', baudrate=9600):
        self.baudrate = baudrate
        self.port = port

    def init(self):
        self.arduino = serial.Serial(port=self.port, baudrate=self.baudrate, timeout=0.1)
        self.arduino.write(str.encode("Initialized"))
        answer = self.arduino.readline()
        print("Arduino connection answer -> {}".format(answer))

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

    def close(self):
        self.arduino.close()
        self.arduino = None


if __name__ == '__main__':
    keyboard = ArduinoKeyboard()
    keyboard.init()

    try:
        while True:
            inp = input("Enter a value: ")
            print("Sending -> {}".format(inp))
            res = keyboard.text(inp)
            print("Received -> {}".format(res))
    except:
        keyboard.close()
