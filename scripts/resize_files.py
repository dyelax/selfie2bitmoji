import os
from glob import glob
from imageio import imread, imwrite
import cv2

paths = glob('../data/bitmoji/*/*.png')

total = len(paths)
for i, path in enumerate(paths):
    img = imread(path)
    new_img = cv2.resize(img, (64, 64), interpolation=cv2.INTER_AREA)
    os.remove(path)
    imwrite(path, new_img)

    print '%d / %d converted' % (i, total)
