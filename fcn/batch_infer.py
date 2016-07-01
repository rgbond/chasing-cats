#!/usr/bin/python
# Takes a list of files
# Saves off the segmented image

import sys
import time
import os

import numpy as np
from PIL import Image

import caffe

caffe.set_mode_gpu()

# load net
net = caffe.Net('voc-fcn32s/deploy.prototxt', 'voc-fcn32s/fcn32s-heavy-pascal.caffemodel', caffe.TEST)
# net = caffe.Net('pascalcontext-fcn32s/deploy.prototxt', 'pascalcontext-fcn32s/pascalcontext-fcn32s-heavy.caffemodel', caffe.TEST)

for i in range(1, len(sys.argv)):
    # load image, switch to BGR, subtract mean, and make dims C x H x W for Caffe
    arg = sys.argv[i]
    im = Image.open(arg)
    in_ = np.array(im, dtype=np.float32)
    in_ = in_[:,:,::-1]
    in_ -= np.array((104.00698793,116.66876762,122.67891434))
    in_ = in_.transpose((2,0,1))

    # shape for input (data blob is N x C x H x W), set data
    net.blobs['data'].reshape(1, *in_.shape)
    net.blobs['data'].data[...] = in_

    # run net and take argmax for prediction
    tic = time.clock()
    net.forward()
    toc = time.clock()
    print "time:", toc-tic

    out = net.blobs['score'].data[0].argmax(axis=0)
    out_8 = np.empty_like(out, dtype=np.uint8)
    np.copyto(out_8, out, casting='unsafe')
    img = Image.fromarray(out_8)

    fn, ext = os.path.splitext(arg)
    if ext == ".jpg":
        img.save(fn + ".png")
        print arg, fn + ".png"
    else:
        print "Was expecting a jpg!", arg
