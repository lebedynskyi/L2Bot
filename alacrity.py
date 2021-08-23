import pyautogui
import time

ALACRITY = "f1"


def alacrity():
    while True:
        print("Loop Alacrity")
        pyautogui.press(ALACRITY)
        time.sleep(1195)


if __name__ == "__main__":
    alacrity()
