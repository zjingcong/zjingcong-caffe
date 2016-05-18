#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
import os

TRAIN_FRAME_FILE = 'Smoke_split_trainFrame.txt'
TEST_FRAME_FILE = 'Smoke_split_testFrame.txt'
TRAIN_VIDEO_FILE = 'Smoke_split_trainVideo.txt'
TEST_VIDEO_FILE = 'Smoke_split_testVideo.txt'


# remove previous split txt file
command = ['rm', TEST_FRAME_FILE, TRAIN_FRAME_FILE]
p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
p.communicate()


# get frame with label via video label file
def label_frame_via_video(video_file, frame_file):
    with open(video_file, 'r') as videoFile:
        videoLabelInfo = videoFile.readlines()

    frame_info = []
    for video_label in videoLabelInfo:
        video_path = video_label.split(' ')[0]
        video_name = video_path.split('/')[-1]
        label = int(video_label.split(' ')[1])

        frame_list = []
        for path in os.walk(video_path):
            if path[0] == video_path:
                frame_list = path[2]
                break
        frame_info.extend(map(lambda x: '{path} {label}\n'.format(path=os.path.join(video_name, x), label=label),
                              frame_list))

    frame_num = len(frame_info)

    # write data into frame label file
    with open(frame_file, 'w') as frameFile:
        frameFile.write(''.join(map(str, frame_info)))

    return frame_num

train_frame_num = label_frame_via_video(TRAIN_VIDEO_FILE, TRAIN_FRAME_FILE)
test_frame_num = label_frame_via_video(TEST_VIDEO_FILE, TEST_FRAME_FILE)
total = train_frame_num + test_frame_num

print "========== Summary =========="
print "# Total Frames: {0}".format(total)
print "# Train Frames: {0}".format(train_frame_num)
print "# Test Frames: {0}".format(test_frame_num)
