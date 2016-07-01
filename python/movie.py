#!/usr/bin/python
# Usage: movie.py f1.jpg f2.jpg f3.png
# Shows a bunch of .png or .jpg files at 1/3 second intervals
# Handy for going through a bunch of images quickly

import sys
import os.path

import numpy as np
import cv2

cv2.namedWindow("movie")
cv2.moveWindow("movie", 300, 300)

if len(sys.argv) == 1:
    exit(0)

for fn in sys.argv[1:]:
    m = cv2.imread(fn)
    if m == None:
        continue
    cv2.imshow('movie', m);
    key = cv2.waitKey(330)
    key = key & 0xff
    if key == 27 or key == ord('q'):
        exit(0)
