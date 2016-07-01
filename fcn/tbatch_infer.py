#!/usr/bin/python
# Stays active, processing files in inbound
# Shuffles files from inbound to classifed as they are processed by the net

import sys
import time
import os

import numpy as np
from PIL import Image

import caffe

def process_file(net, arg, inbound, classified):
    src = os.path.join(inbound, arg)
    dest = os.path.join(classified, arg)
    # load image, switch to BGR, subtract mean, and make dims C x H x W for Caffe

    try:
        im = Image.open(os.path.join(inbound, arg))
        in_ = np.array(im, dtype=np.float32)
    except IOError:
        print "IOError on:", src
        os.remove(src);
        return
    except SystemError:
        print "SystemError on:", src
        os.remove(src);
        return

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

    # out = net.blobs['score'].data[0].argmax(axis=0)
    out = net.blobs['my_score'].data[0].argmax(axis=0)
    out_8 = np.empty_like(out, dtype=np.uint8)
    np.copyto(out_8, out, casting='unsafe')
    img = Image.fromarray(out_8)

    fn, ext = os.path.splitext(dest)
    if ext == ".jpg":
        img.save(fn + ".png")
        os.rename(src, dest)
        print arg, fn + ".png"
    else:
        print "Was expecting a jpg!", arg

if __name__ == "__main__":
    caffe.set_mode_gpu()

    # load net
    net = caffe.Net('voc-fcn32s/deploy.prototxt', 'voc-fcn32s/fcn32s-heavy-pascal.caffemodel', caffe.TEST)

    inbound = "/caffe/inbound"
    classified = "/caffe/classified"
    while True:
        to_process = os.listdir(inbound)
        if to_process == []:
            # seem to have to keep it warm or we get timeouts
            net.forward()
        else:
            to_process.sort()
            for arg in to_process:
                print "Processing:", arg
                process_file(net, arg, inbound, classified)
