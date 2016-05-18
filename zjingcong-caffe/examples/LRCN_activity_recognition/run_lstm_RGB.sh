#!/bin/bash

TOOLS=/home/zjc/workspace/git/zjingcong-caffe/zjingcong-caffe/build/tools

export HDF5_DISABLE_VERSION_CHECK=1
export PYTHONPATH=.

LOG=/home/zjc/log/run_lstm_RGB_log/train-$(date +%Y-%m-%d-%H:%M).log

echo "LOG PATH: "
echo $LOG
GLOG_logtostderr=1  $TOOLS/caffe train -solver lstm_solver_RGB.prototxt -weights /disk/zjingcong/caffemodel/caffe_imagenet_hyb2_wr_rc_solver_sqrt_iter_310000 > $LOG 2>&1
echo "Done."
