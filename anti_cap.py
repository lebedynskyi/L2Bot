import os
from app.App import App

current_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "screen.png")

if __name__ == "__main__":
    app = App(current_path)
    app.tick()
