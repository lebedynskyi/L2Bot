import os

from tools import color_tools as cl

if __name__ == "__main__":
    cwd = os.getcwd()
    bmp = os.path.join(cwd, "res/color_source.bmp")
    cl.run_color_picker(bmp)