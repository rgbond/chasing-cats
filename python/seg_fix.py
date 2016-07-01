#!/usr/bin/python
# argv[1] is the dest. directory
# All arguments past that are source .png files
# An example of how to remap the segments in an image

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
    if src_ext != ".png":
        print "Bad file name:", src
        continue
    dest  = os.path.join(dest_dir, src_fn + '.png')
    print src, dest
    im = Image.open(src)
    mat = np.array(im, dtype=np.uint8)
    fixed_mat = np.zeros_like(mat, dtype=np.uint8)
    for i in range(60, 76):
        fixed_mat[mat == i] = i - 60 + 1
    im = Image.fromarray(fixed_mat)
    im.save(dest)
