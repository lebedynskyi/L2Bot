import cv2 as cv
import numpy as np
import os
from matplotlib import pyplot as plt

parse_methods = methods = ['cv.TM_CCOEFF', 'cv.TM_CCOEFF_NORMED', 'cv.TM_CCORR',
                           'cv.TM_CCORR_NORMED', 'cv.TM_SQDIFF', 'cv.TM_SQDIFF_NORMED']


def _find_dialog(original, template):
    img = original.copy()
    w, h = template.shape[::-1]

    img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    res = cv.matchTemplate(img_gray, template, cv.TM_CCOEFF_NORMED)
    threshold = 0.8
    loc = np.where(res >= threshold)
    dialog_points = list(zip(*loc[::-1]))
    if not dialog_points:
        print("No dialog found")
        return
    else:
        print("Found bot dialog")
        for pt in dialog_points:
            cv.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)

    plt.title('Detected dialog'), plt.xticks([]), plt.yticks([])
    plt.imshow(img)
    plt.show()

    cv.imwrite('res.png', img)


class AntiBotParser:
    def __init__(self):
        pass

    def parse(self, input, template):
        if not os.path.exists(input):
            raise FileNotFoundError(input)

        if not os.path.exists(template):
            raise FileNotFoundError(template)

        print("Parsing file -> %s" % input)

        img = cv.imread(input, )
        template = cv.imread(template, cv.IMREAD_GRAYSCALE)
        _find_dialog(img.copy(), template)
