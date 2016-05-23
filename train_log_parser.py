#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Usage: python train_log_parser.py <net_type> <log_name>
# <net_type>: 'lstm' or 'single'

import matplotlib.pyplot as plt
import sys
import re
import os

if len(sys.argv) == 3:
    TYPE = sys.argv[1]
    if TYPE == 'lstm':
        TRAINLOGPATH = '/home/zjc/log/run_lstm_RGB_log'
    elif TYPE == 'single':
        TRAINLOGPATH = '/home/zjc/log/run_singleFrame_RGB_log'
    LOGNAME = sys.argv[2]
    LOGPATH = os.path.join(TRAINLOGPATH, LOGNAME)
else:
    print "Check argv."
    sys.exit(1)


# parse accuracy and loss for train net and test net
def extract_number(text):
    for m in re.finditer(r'[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?', text):
        yield float(m.group(0))

with open(LOGPATH, 'r') as log_file:
    log_info = log_file.readlines()

# initialization
test_summary = dict()
train_summary = dict()
lr_summary = dict()
test_summary['iter'] = []
train_summary['iter'] = []
test_summary['accuracy'] = []
train_summary['accuracy'] = []
test_summary['loss'] = []
train_summary['loss'] = []
lr_summary['iter'] = []
lr_summary['lr'] = []

for index, line_info in enumerate(log_info):
    if index + 3 > len(log_info):
        continue

    # get test info
    if re.search(r'Iteration \d+, Testing net', line_info):
        if 'Test net output' in log_info[index + 1]:
            test_iter = int(list(extract_number(line_info.split(']')[1]))[0])
            accuracy = list(extract_number(log_info[index + 1].split(']')[1]))[1]
            test_summary['iter'].append(test_iter)
            test_summary['accuracy'].append(accuracy)
            if 'Test net output' in log_info[index + 2]:
                loss = list(extract_number(log_info[index + 2].split(']')[1]))[1]
                test_summary['loss'].append(loss)

    # get train info
    elif re.search(r'Iteration \d+, loss = \d*', line_info):
        if 'Train net output' in log_info[index + 1]:
            train_iter = int(list(extract_number(line_info.split(']')[1]))[0])
            accuracy = list(extract_number(log_info[index + 1].split(']')[1]))[1]
            train_summary['iter'].append(train_iter)
            train_summary['accuracy'].append(accuracy)
            if 'Train net output' in log_info[index + 2]:
                loss = list(extract_number(log_info[index + 2].split(']')[1]))[1]
                train_summary['loss'].append(loss)

    # get lr info
    elif re.search(r'Iteration \d+, lr = \d*', line_info):
        lr_iter = int(list(extract_number(line_info.split(']')[1]))[0])
        lr = float(list(extract_number(line_info.split(']')[1]))[1])
        lr_summary['iter'].append(lr_iter)
        lr_summary['lr'].append(lr)

# plot accuracy for test phase and train phase and save the figures
# accuracy
accuracy_figure = plt.figure('Accuracy')
ax1_train_test = accuracy_figure.add_subplot(111)
ax1_train_test.plot(train_summary['iter'], train_summary['accuracy'], 'g', label='train')
ax1_train_test.plot(test_summary['iter'], test_summary['accuracy'], 'r', label='test')
ax1_lr = ax1_train_test.twinx()
ax1_lr.plot(lr_summary['iter'], lr_summary['lr'], 'b', label='lr')

ax1_train_test.legend(loc=3)
ax1_lr.legend(loc=8)

if TYPE == 'lstm':
    plt.savefig('/home/zjc/log/run_lstm_RGB_log/accuracy-{0}.jpg'.format(LOGNAME[: -4]))
elif TYPE == 'single':
    plt.savefig('/home/zjc/log/run_singleFrame_RGB_log/accuracy-{0}.jpg'.format(LOGNAME[: -4]))

# loss
loss_figure = plt.figure('Loss')
ax2_train_test = loss_figure.add_subplot(111)
ax2_train_test.plot(train_summary['iter'], train_summary['loss'], 'g', label='train')
ax2_train_test.plot(test_summary['iter'], test_summary['loss'], 'r', label='test')
ax2_lr = ax2_train_test.twinx()
ax2_lr.plot(lr_summary['iter'], lr_summary['lr'], 'b', label='lr')

ax2_train_test.legend(loc=1)
ax2_lr.legend(loc=9)

if TYPE == 'lstm':
    plt.savefig('/home/zjc/log/run_lstm_RGB_log/loss-{0}.jpg'.format(LOGNAME[: -4]))
elif TYPE == 'single':
    plt.savefig('/home/zjc/log/run_singleFrame_RGB_log/loss-{0}.jpg'.format(LOGNAME[: -4]))

plt.show()
