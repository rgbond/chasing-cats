import caffe
import surgery, score

import numpy as np
import os

import setproctitle
setproctitle.setproctitle(os.path.basename(os.getcwd()))

weights = 'rgb_voc_fcn32s/train_iter_96000.caffemodel'

# init
caffe.set_device(0)
caffe.set_mode_gpu()

solver = caffe.SGDSolver('rgb_voc_fcn32s/solver.prototxt')
solver.net.copy_from(weights)

# surgeries
interp_layers = [k for k in solver.net.params.keys() if 'up' in k]
surgery.interp(solver.net, interp_layers)

# scoring
val = np.loadtxt('data/rgb_voc/segvalid.txt', dtype=str)

# Skip the loop (commented out below)
solver.step(4000) 
score.seg_tests(solver, False, val, layer='my_score')

# for _ in range(25):
#     solver.step(4000)
#     score.seg_tests(solver, False, val, layer='my_score')
