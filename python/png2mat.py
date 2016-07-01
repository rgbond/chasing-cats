#!/usr/bin/python
# Converts a .png segmented image to a .mat segmented image

import sys
import scipy.io as sio
import numpy as np
from PIL import Image

src = sys.argv[1]
dest = sys.argv[2]

im = Image.open(src)
m = np.array(im, dtype=np.uint16)
sio.savemat(dest, {'LabelMap':m})
