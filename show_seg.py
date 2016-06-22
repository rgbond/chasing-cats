#!/usr/bin/python
# Usage: show_seg src.jpg seg.png 
#

import sys
import os.path

import numpy as np
import cv2

palette = []
r = [0, 224, 32, 192, 64, 160, 128]
for i in range(7):
    for j in range(7):
        for k in range(7):
            palette += [[r[k], r[j], r[i]]]


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
