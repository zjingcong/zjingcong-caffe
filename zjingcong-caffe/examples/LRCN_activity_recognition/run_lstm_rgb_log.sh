#! /bin/bash

LOG=/home/zjc/log/run_lstm_RGB_log/train-$(date +%Y-%m-%d-%M:%m).log

echo "LOG PATH: "
echo $LOG
/bin/bash run_lstm_RGB.sh > $LOG 2>&1
