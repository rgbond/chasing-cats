#!/usr/bin/python
# Call with .mat files on the command line
# Understands the pascal voc segmentation used in the sdb .mat segmenations
# Exmaple:
# $ count_pascal_mat.py sdb/benchmark_RELEASE/dataset/cls/2008_006606.mat
# sdb/benchmark_RELEASE/dataset/cls/2008_006606.mat    none 142076    chair 17106    tvmonitor 7318


import sys
import time

import numpy as np
import scipy.io as sio

import caffe

labels = [ "none", "aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat", "chair", "cow", "table", "dog",
    "horse", "motorbike", "person", "pottedplant", "sheep", "sofa", "train", "tvmonitor",

    "bag", "bed", "bench", "book", "building", "cabinet", "ceiling", "cloth", "computer", "cup", "door", "fence", "floor",
    "flower", "food", "grass", "ground", "keyboard", "light", "mountain", "mouse", "curtain", "platform", "sign",
    "plate", "road", "rock", "shelves", "sidewalk", "sky", "snow", "bedclothes", "track", "tree", "truck",
    "wall", "water", "window", "wood"
    ]

def dump_counts(out):
    count = np.zeros(500, np.uint32)
    cols = out.shape[0]
    rows = out.shape[1]
    for y in range(cols):
        for x in range(rows):
            v = out[y, x]
            count[v] += 1
    for i in range(len(count)):
        if count[i] > 0:
            if (i < len(labels)):
                print "  ", labels[i], count[i],
            else:
                print "  ", i, count[i],
    print

for i in range(1, len(sys.argv)):
    mat = sio.loadmat(sys.argv[i])
    mat = mat['GTcls'][0]['Segmentation'][0].astype(np.uint8)
    print sys.argv[i],
    dump_counts(mat)
