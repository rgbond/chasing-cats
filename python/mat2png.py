#!/usr/bin/python
# argv[1] is the dest. directory
# Converts a lsit of sdb segmented .mat files to .png files.
# All arguments past that are source .mat files

import sys
import os.path

import numpy as np
import scipy.io as sio
from PIL import Image

dest_dir = sys.argv[1]
for i in range(2, len(sys.argv)):
    src = sys.argv[i]
    src_base = os.path.basename(src)
    src_fn, src_ext = os.path.splitext(src_base)
    if src_ext != ".mat":
        print "Bad file name:", src
        continue
    dest  = os.path.join(dest_dir, src_fn + '.png')
    print src, dest
    mat = sio.loadmat(sys.argv[i])
    mat = mat['GTcls'][0]['Segmentation'][0].astype(np.uint8)
    im = Image.fromarray(mat)
    im.save(dest)
