#!/usr/bin/python
# Resizes an image to 640x360

import os, sys
from PIL import Image

size = (640, 360)

for fn in sys.argv[1:]:
    try:
        im = Image.open(fn)
        im = im.resize(size, Image.BICUBIC)
        im.save(fn)
    except IOError:
        print "oops"
