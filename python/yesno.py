#!/usr/bin/python
# Usage: yesno.py file_list
# Handy util used to bucket images.
# Pass in a list of images on the command line. Output is two files, yes, and no. 

import sys
import os.path

import numpy as np
import cv2

cv2.namedWindow("yesno")
cv2.moveWindow("yesno",300, 300)

for fn in sys.argv[1:]:
    m = cv2.imread(fn)
    cv2.imshow('yesno', m);

    key = cv2.waitKey(0)
    key = key & 0xff
    if key == 27 or key == ord('q'):
        exit(0)
    elif key == ord('y'):
        with open("yes", 'a') as f:
            f.write(fn + '\n')
    else:
        with open("no", 'a') as f:
            f.write(fn + '\n')
        
        
