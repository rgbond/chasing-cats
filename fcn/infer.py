#!/usr/bin/python
# Just like the Shellhammer version except it saves the segmented file

import sys
import time

import numpy as np
from PIL import Image

import caffe

# load image, switch to BGR, subtract mean, and make dims C x H x W for Caffe
caffe.set_mode_gpu()

im = Image.open(sys.argv[1])
in_ = np.array(im, dtype=np.float32)
in_ = in_[:,:,::-1]
in_ -= np.array((104.00698793,116.66876762,122.67891434))
in_ = in_.transpose((2,0,1))

# load net
# net = caffe.Net('voc-fcn-alexnet/deploy.prototxt', 'voc-fcn-alexnet/fcn-alexnet-pascal.caffemodel', caffe.TEST)
# net = caffe.Net('voc-fcn8s/deploy.prototxt', 'voc-fcn8s/fcn8s-heavy-pascal.caffemodel', caffe.TEST)
# net = caffe.Net('voc-fcn32s/deploy.prototxt', 'voc-fcn32s/fcn32s-heavy-pascal.caffemodel', caffe.TEST)
# net = caffe.Net('pascalcontext-fcn32s/deploy.prototxt', 'pascalcontext-fcn32s/pascalcontext-fcn32s-heavy.caffemodel', caffe.TEST)
net = caffe.Net('rgb_voc_fcn32s/deploy.prototxt', 'rgb_voc_fcn32s/train_iter_4000.caffemodel', caffe.TEST)

# shape for input (data blob is N x C x H x W), set data
net.blobs['data'].reshape(1, *in_.shape)
net.blobs['data'].data[...] = in_

# run net and take argmax for prediction
tic = time.clock()
net.forward()
toc = time.clock()
print toc-tic

# And again for fun
tic = time.clock()
net.forward()
toc = time.clock()
print toc-tic

# out = net.blobs['score'].data[0].argmax(axis=0)
out = net.blobs['score'].data[0].argmax(axis=0)
out_8 = np.empty_like(out, dtype=np.uint8)
np.copyto(out_8, out, casting='unsafe')
img = Image.fromarray(out_8)
img.save("infer_out.png")
