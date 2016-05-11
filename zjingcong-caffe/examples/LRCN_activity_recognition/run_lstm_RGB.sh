#!/bin/bash

TOOLS=/home/zjc/workspace/git/zjingcong-caffe/zjingcong-caffe/build/tools

export HDF5_DISABLE_VERSION_CHECK=1
export PYTHONPATH=.

GLOG_logtostderr=1  $TOOLS/caffe train -solver lstm_solver_RGB.prototxt -weights /disk/zjingcong/caffemodel/caffe_imagenet_hyb2_wr_rc_solver_sqrt_iter_310000  
echo "Done."
