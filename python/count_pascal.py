#!/usr/bin/python
# Dump the counts in a pascal context segmentation as converted by mat2png.py
# Example:
# $ count_pascal.py /images/sdb_seg/2009_001133.png
# none 0 65781
# sofa 18 109776
# train 19 13443
#

import sys
import time

import numpy as np
from PIL import Image

import caffe

labels = [ "none", "aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat", "chair", "cow", "table", "dog",
    "horse", "motorbike", "person", "pottedplant", "sheep", "sofa", "train", "tvmonitor",

    "bag", "bed", "bench", "book", "building", "cabinet", "ceiling", "cloth", "computer", "cup", "door", "fence", "floor",
    "flower", "food", "grass", "ground", "keyboard", "light", "mountain", "mouse", "curtain", "platform", "sign",
    "plate", "road", "rock", "shelves", "sidewalk", "sky", "snow", "bedclothes", "track", "tree", "truck",
    "wall", "water", "window", "wood"
    ]

def dump_counts(out):
    count = np.zeros(len(labels), np.uint32)
    cols = out.shape[0]
    rows = out.shape[1]
    for y in range(cols):
        line = ""
        for x in range(rows):
            v = out[y, x]
            count[v] += 1
            s = str(v)
            line += s
        # print line
    for i in range(len(labels)):
        if count[i] > 0:
            print labels[i], i, count[i]

im = Image.open(sys.argv[1])
in_ = np.array(im, dtype=np.uint8)
dump_counts(in_)
