#!/usr/bin/env python
# -*- coding: utf-8 -*-

import yaml
import subprocess

LABEL_FILE = 'label_video.yaml'
TRAIN_VIDEO_FILE = 'Smoke_split_trainVideo.txt'
TEST_VIDEO_FILE = 'Smoke_split_testVideo.txt'


command = ['touch', TEST_VIDEO_FILE, TRAIN_VIDEO_FILE]
p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
p.communicate()

f = file(LABEL_FILE, 'r')
video_list = yaml.load(f)
class_list = list(set([i.get('class') for i in video_list]))

test_data_num = 0
train_data_num = 0
total = 0

with open(TEST_VIDEO_FILE, 'r') as f:
    test = f.readlines()
with open(TRAIN_VIDEO_FILE, 'r') as f:
    train = f.readlines()
dataset = test + train

print "\nAdd Train Data and Test Data..."
print "*****************************"
for video_class in class_list:
    video_per_class = ['{path} {label}\n'.format(path=i.get('path'), label=i.get('label')) for i in video_list
                       if i.get('class') == video_class
                       and '{path} {label}\n'.format(path=i.get('path'), label=i.get('label')) not in dataset]
    num = len(video_per_class)
    test_num = int(num / 3)
    train_num = num - test_num
    test_data_num += test_num
    train_data_num += train_num
    total += num
    print "{0} | Total: {1}, Train: {2}, Test: {3}".format(video_class, num, train_num, test_num)

    train_data = ''.join(map(str, video_per_class[0: train_num]))
    test_data = ''.join(map(str, video_per_class[train_num: num]))
    with open(TRAIN_VIDEO_FILE, 'a') as train_file:
        train_file.write(train_data)
    with open(TEST_VIDEO_FILE, 'a') as test_file:
        test_file.write(test_data)

print "*****************************"
print "# Total New Videos: {0}".format(total)
print "# Train New Videos: {0}".format(train_data_num)
print "# Test New Videos: {0}".format(test_data_num)

with open(TRAIN_VIDEO_FILE, 'r') as f:
    total_train = len(f.readlines())
with open(TEST_VIDEO_FILE, 'r') as f:
    total_test = len(f.readlines())
total_video = total_train + total_test

print "========== Summary =========="
print "# Total Videos: {0}".format(total_video)
print "# Train Videos: {0}".format(total_train)
print "# Test Videos: {0}".format(total_test)
