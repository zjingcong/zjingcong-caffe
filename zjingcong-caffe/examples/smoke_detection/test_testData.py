#!/usr/bin/env python
# -*- coding: utf-8 -*-

from classify_video import videoClassifier

TEST_FILE = '/home/zjc/workspace/git/zjingcong-caffe/Smoke_split_testVideo.txt'
gpu_id = 0

with open(TEST_FILE, 'r') as test_video_file:
    test_info = test_video_file.readlines()

print "Test videos: {0}".format(len(test_info))
print '=' * 40
result_list = []
for video_info in test_info:
    result = 1  # 1: success, 0: fail
    print '=' * 40
    video_path = video_info.split(' ')[0]
    label = int(video_info.split(' ')[1])
    print "Classify video: {0}...".format(video_path)
    class_RGB_LRCN = videoClassifier(video_path, gpu_id)
    print "Real: {0}".format(label)
    print "LRCN: {0}".format(class_RGB_LRCN)
    if class_RGB_LRCN == label:
        print "Classification success."
        result = 1
    else:
        print "Classification fail."
        result = 0
    result_list.append(result)

print "=================== Summary =================="
total = len(result_list)
correct = sum(result_list)
error = total - correct
success_rate = float(correct) / total
error_rate = float(error) / total
print "# Total: ", total
print "# Correct: ", correct
print "# Error: ", error
print "# Success Rate: ", success_rate
print "# False Rate: ", error_rate
