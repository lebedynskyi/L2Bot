import cv2
import numpy as np
from PIL import Image


def read_input_img(path):
    gbr = Image.open(path)
    gbr_arr = np.array(gbr)
    rgb_arr = cv2.cvtColor(gbr_arr, cv2.COLOR_BGR2RGB)
    grey = cv2.cvtColor(rgb_arr, cv2.COLOR_RGB2GRAY)

    return rgb_arr, grey
