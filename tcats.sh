#!/bin/bash
cd /caffe/fcn*
echo staring dclean
dclean.sh &
echo starting caffe
./tbatch_infer.py >> caffe.out 2>&1 &
echo starting tcats.py
tcats.py
