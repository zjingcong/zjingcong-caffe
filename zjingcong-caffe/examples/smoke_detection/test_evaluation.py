#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Classify the whole test dataset and calculate the accuracy
# Usage: python test_evaluation.py <test_file_path> <gpu_id> <lstm_caffemodel> <evaluation_mode>

from classify_video import videoClassifier

import pprint
import sys

'''
test_file_path = '/home/zjc/workspace/backup/test_train_txtFile_backup/' \
                 'lstm-train-2016-05-22-20:05/Smoke_split_testVideo.txt'
gpu_id = 0
lstm_model = 'snapshots_lstm_RGB_iter_1600.caffemodel'
'''

if len(sys.argv) > 3:
    test_file_path = sys.argv[1]
    gpu_id = sys.argv[2]
    lstm_model = sys.argv[3]
else:
    print "Check argv: [USAGE]python test_evaluation.py <test_file_path> <gpu_id> <lstm_caffemodel>"
    sys.exit(1)

with open(test_file_path, 'r') as test_file:
    test_info_list = test_file.readlines()


def is_correct(real_label, result):
    if real_label == result:
        return 1
    else:
        return 0

# test_info_list: <list>[<tuple>(<str>video_path, <int>label)]
test_info_list = map(lambda x: (x.split(' ')[0], int(x.split(' ')[1])), test_info_list)
# label_result: <list>[<tuple>(<int>is_correct, <str>video_path)]
label_result = map(lambda x: (is_correct(x[1], videoClassifier(x[0])[0]), x[0]), test_info_list)

# summary
correct = len([i for i in label_result if i[0] == 1])
total = len(label_result)
error = total - correct
error_video_list = [i[1].split('/')[-1] for i in label_result if i[0] == 0]
correct_video_list = [i[1].split('/')[-1] for i in label_result if i[0] == 1]
print "=================== Evaluation Summary ==================="
print "# Total Videos: ", total
print "# Correct Videos: ", correct
print "# Error Videos: ", error
print "# Accuracy: ", float(correct) / total
print "# Correct Videos List: "
pprint.pprint(correct_video_list)
print "# Error Videos List: "
pprint.pprint(error_video_list)
