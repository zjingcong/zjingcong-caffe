#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Usage: run after generating label_video.yaml file

import yaml
import subprocess
import random

LABEL_FILE = 'label_video.yaml'
TRAIN_VIDEO_FILE = 'Smoke_split_trainVideo.txt'
TEST_VIDEO_FILE = 'Smoke_split_testVideo.txt'


# remove previous split txt file
command = ['rm', TEST_VIDEO_FILE, TRAIN_VIDEO_FILE]
p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
p.communicate()

# get video classes
f = file(LABEL_FILE, 'r')
video_list = yaml.load(f)
class_list = list(set([i.get('class') for i in video_list]))

test_data_num = 0
train_data_num = 0
total = 0

train_total_list = []
test_total_list = []

print "\nGet Train Data and Test Data..."
print '=' * 29
for video_class in class_list:
    video_per_class = ['{path} {label}\n'.format(path=i.get('path'), label=i.get('label')) for i in video_list
                       if i.get('class') == video_class]
    num = len(video_per_class)
    test_num = int(num / 3)
    train_num = num - test_num
    if num == 2:
        test_num = 1
        train_num = 1

    test_data_num += test_num
    train_data_num += train_num
    total += num
    print "{0} | Total: {1}, Train: {2}, Test: {3}".format(video_class, num, train_num, test_num)

    train_list = video_per_class[0: train_num]
    test_list = video_per_class[train_num: num]

    train_total_list.extend(train_list)
    test_total_list.extend(test_list)

# Shuffle the train data and test data
random.shuffle(train_total_list)
random.shuffle(test_total_list)

# write the train and test data to txt file
train_data = ''.join(map(str, train_total_list))
test_data = ''.join(map(str, test_total_list))
with open(TRAIN_VIDEO_FILE, 'w') as train_file:
    train_file.write(train_data)
with open(TEST_VIDEO_FILE, 'w') as test_file:
    test_file.write(test_data)

print "========== Summary =========="
print "# Total Videos: {0}".format(total)
print "# Train Videos: {0}".format(train_data_num)
print "# Test Videos: {0}".format(test_data_num)
