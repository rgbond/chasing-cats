#!/usr/bin/python
# Usage: show_seg src.jpg seg.png 
# Shows the segmentation, given a base image and a segment
# Picks a random palette.
# Use the 't' key to toggle between the two

import sys
import os.path
import random

import numpy as np
import cv2

r = [0, 224, 32, 192, 64, 160, 128]
def rn():
    return r[random.randint(0, 6)]

palette = [[0, 0, 0]]
random.seed(2)
for i in range(1, 256):
    v = [rn(), rn(), rn()]
    while v in palette:
        v = [rn(), rn(), rn()]
    palette += [v]

if len(sys.argv) == 3:
    # Get filenames
    src_fn = sys.argv[1]
    seg_fn = sys.argv[2]

    src_mat = cv2.imread(src_fn, flags = 1)
    seg_mat = cv2.imread(seg_fn, flags = 0)

    # Paint src pixels
    src_pmat = src_mat.copy()
    for i in range(1, 256):
        src_pmat[seg_mat == i] = palette[i]

    cv2.namedWindow("show_seg")
    cv2.moveWindow("show_seg", 300, 300)

    cv2.imshow('show_seg', src_pmat);
    show_painted = True

    while True:
        key = cv2.waitKey(1)
        key = key & 0xff
        if key == 27 or key == ord('q'):
            exit(0)
        if key == ord('t'):
            show_painted = not show_painted
            if show_painted:
                cv2.imshow("show_seg", src_pmat)
            else:
                cv2.imshow("show_seg", src_mat)
