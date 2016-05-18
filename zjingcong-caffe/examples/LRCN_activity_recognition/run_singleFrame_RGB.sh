#!/bin/sh

TOOLS=/home/zjc/workspace/git/zjingcong-caffe/zjingcong-caffe/build/tools
LOG=/home/zjc/log/run_singleFrame_RGB_log/single-train-$(date +%Y-%m-%d-%H:%M).log

echo "LOG PATH: "
echo $LOG
GLOG_logtostderr=1 $TOOLS/caffe train -solver singleFrame_solver_RGB.prototxt -weights /disk/zjingcong/caffemodel/caffe_imagenet_hyb2_wr_rc_solver_sqrt_iter_310000 > $LOG 2>&1
echo 'Done.'
