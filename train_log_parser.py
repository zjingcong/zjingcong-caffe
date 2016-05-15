#!/usr/bin/env python
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import sys
import re
import os

TRAINLOGPATH = '/home/zjc/log/run_lstm_RGB_log'

if len(sys.argv) == 2:
    LOGPATH = os.path.join(TRAINLOGPATH, sys.argv[1])
else:
    print "Check argv."
    sys.exit(1)


# parse accuracy and loss for train net and test net
def extract_number(text):
    for m in re.finditer(r'[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?', text):
        yield float(m.group(0))

with open(LOGPATH, 'r') as log_file:
    log_info = log_file.readlines()

test_summary = dict()
train_summary = dict()
test_summary['iter'] = []
train_summary['iter'] = []
test_summary['accuracy'] = []
train_summary['accuracy'] = []
test_summary['loss'] = []
train_summary['loss'] = []

for index, line_info in enumerate(log_info):
    if re.search(r'Iteration \d+, Testing net', line_info):
        if 'Test net output' in log_info[index + 1]:
            test_iter = int(list(extract_number(line_info.split(']')[1]))[0])
            accuracy = list(extract_number(log_info[index + 1].split(']')[1]))[1]
            loss = list(extract_number(log_info[index + 2].split(']')[1]))[1]
            test_summary['iter'].append(test_iter)
            test_summary['accuracy'].append(accuracy)
            test_summary['loss'].append(loss)

    elif re.search(r'Iteration \d+, loss = \d*', line_info):
        if 'Train net output' in log_info[index + 1]:
            train_iter = int(list(extract_number(line_info.split(']')[1]))[0])
            accuracy = list(extract_number(log_info[index + 1].split(']')[1]))[1]
            loss = list(extract_number(log_info[index + 2].split(']')[1]))[1]
            train_summary['iter'].append(train_iter)
            train_summary['accuracy'].append(accuracy)
            train_summary['loss'].append(loss)

# plot accuracy for test phase and train phase
plt.figure(1)
plt.plot(test_summary['iter'], test_summary['accuracy'], 'r')
plt.plot(train_summary['iter'], train_summary['accuracy'], 'g')
plt.show()
