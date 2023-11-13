from tkinter import Image

import cv2
import numpy as np
from PIL import Image


def read_input_img(path):
    bgr = Image.open(path)
    bgr_arr = np.array(bgr)
    rgb = cv2.cvtColor(bgr_arr, cv2.COLOR_BGR2RGB)
    grey = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)

    return rgb, grey
