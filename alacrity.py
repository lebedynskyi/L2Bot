import pyautogui
import time

ALACRITY = "f10"


def alacrity():
    time.sleep(3)

    while True:
        print("Loop Alacrity")
        pyautogui.press(ALACRITY)
        time.sleep()


if __name__ == "__main__":
    alacrity()
