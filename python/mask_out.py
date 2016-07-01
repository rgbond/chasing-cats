#!/usr/bin/python
# mask_out file.jpg file.png
# file.png should have a set of pascal voc segments. Replaces the png file
# with a masked version of the .jpg
palette = [
    [0,0,0],
    [128,0,0],
    [0,128,0],
    [128,128,0],
    [0,0,128],
    [128,0,128],
    [0,128,128],
    [128,128,128],
    [64,0,0],
    [192,0,0],
    [64,128,0],
    [192,128,0],
    [64,0,128],
    [192,0,128],
    [64,128,128],
    [192,128,128],
    [0,64,0],
    [128,64,0],
    [0,192,0],
    [128,192,0],
    [0,64,128]
]

import sys
import os
from PIL import Image 
import numpy as np

jpg_fn = sys.argv[1]
mask_fn = sys.argv[2]

image = Image.open(jpg_fn)
image = np.array(image, dtype=np.uint8)

mask = Image.open(mask_fn)
mask = np.array(mask, dtype=np.uint8)

for i in range(1, len(palette)):
    image[mask == i] = palette[i]

image = Image.fromarray(image)
image.save(mask_fn)
