#!/usr/bin/env python
# -*- coding: utf-8 -*-

from classify_video import videoClassifier

import pprint

test_file_path = '/home/zjc/workspace/backup/test_train_txtFile_backup/' \
                 'lstm-train-2016-05-22-20:05/Smoke_split_testVideo.txt'
gpu_id = 0

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
error_video_list = [i[1] for i in label_result if i[0] == 0]
print "=================== Evaluation Summary ==================="
print "# Total Videos: ", total
print "# Correct Videos: ", correct
print "# Error Videos: ", error
print "# Accuracy: ", float(correct) / total
print "# Error Videos List: "
pprint.pprint(error_video_list)
