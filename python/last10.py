#!/usr/bin/python
# Usage: last10.py
# Shows the last 10 shots at 1/2 res
# Keys:
#   j: show only .jpgs
#   p: show only .pngs
#   b: show both .jpg and .pngs. Default.
#

import sys
import os
import os.path as p

import numpy as np
import cv2

raw="/caffe/outbound/raw"
r = 160
c = 320
a = np.zeros((r * 5, c * 2, 3), dtype=np.uint8)
jpegs = True
pngs = True

def pick_file(flist, fi):
    gotone = False
    while fi >= 0 and not gotone:
        fn = flist[fi]
        fn1, ext = p.splitext(fn)
        if jpegs and ext == ".jpg":
            gotone = True
        elif pngs and ext == ".png":
            gotone = True
        fi -= 1
    if gotone:
        return fi, fn
    else:
        return fi, None

while True:
    flist = os.listdir(raw)
    flist.sort()
    fi = len(flist) - 1
    for x in [1, 0]:
        for y in [4, 3, 2, 1, 0]:
            fi, fn = pick_file(flist, fi)
            if fn:
                m = cv2.imread(raw + "/" + fn)
                if m != None:
                    a[y*r:(y+1)*r, x*c:(x+1)*c] = cv2.resize(m, (c, r))

    cv2.imshow("Last 10", a)

    key = cv2.waitKey(10000)
    if key == 27 or key == ord('q'):
        exit(0)
    elif key == ord('j'):
        jpegs = True
        pngs = False
    elif key == ord('p'):
        jpegs = False
        pngs = True
    elif key == ord('b'):
        jpegs = True
        pngs = True
