#!/usr/bin/python
# Usage: [-t ms] movie file_list
# Shows a bunch of .png or .jpg files at 1/3 second intervals
# Handy for going through a bunch of images quickly
# -t - set delay between frames.
#

import sys
import os.path

import numpy as np
import cv2

cv2.namedWindow("movie")
cv2.moveWindow("movie", 300, 300)

if len(sys.argv) == 1:
    exit(0)

t = 330
ai = 1
if sys.argv[1] == "-t":
    t = int(sys.argv[2])
    ai += 2

for fn in sys.argv[ai:]:
    m = cv2.imread(fn)
    if m == None:
        continue
    cv2.imshow('movie', m);
    key = cv2.waitKey(t)
    key = key & 0xff
    if key == 27 or key == ord('q'):
        exit(0)
    elif key == ord('p'):
        print fn
