import pyautogui
import time

TARGET = "f1"
SPOIL = "f2"
MANOR = "f3"
PICK = "f4"
HARVESTER = "f5"
SWEEPER = "f6"


def boto_spoil():
    time.sleep(2)
    while True:
        print("Loop Spoil - Manor")
        pyautogui.press(TARGET)
        time.sleep(0.1)

        pyautogui.press(SPOIL)
        time.sleep(0.2)
        pyautogui.press(MANOR)

        time.sleep(2)

        pyautogui.press(HARVESTER)
        time.sleep(0.2)
        pyautogui.press(SWEEPER)
        time.sleep(0.2)
        pyautogui.press(PICK)


if __name__ == "__main__":
    boto_spoil()
