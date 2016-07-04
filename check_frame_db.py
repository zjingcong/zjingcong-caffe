#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Usage: Nothing to do. Plz ignore it.

import os
from PIL import Image
import traceback
import pprint

FRAME_DB_PATH = '/disk/zjingcong/frame_db'
TRAIN_LSTM_FILE = 'Smoke_split_trainVideo.txt'
TEST_LSTM_FILE = 'Smoke_split_testVideo.txt'
CONV_FRAME_BK_PATH = '/disk/zjingcong/conv_mirror'


'''
frame_db_dict = dict()
video_in_db_list = []
for path in os.walk(FRAME_DB_PATH):
    if path[0] == FRAME_DB_PATH:
        video_in_db_list = map(lambda x: os.path.join(FRAME_DB_PATH, x), path[1])
        continue
    video = path[0]
    # video_name = video.split('/')[-1]
    frame_list = path[2]
    frame_db_dict[video] = len(frame_list)

# check conv frame num
for video_name in frame_db_dict:
    if video_name.startswith('conv-mirror-'):
        origin_video_name = video_name[12:]
        if frame_db_dict[video_name] != frame_db_dict[origin_video_name]:
            print "Frame num doesn't match | conv_video: {0}, origin_video: {1}".format(origin_video_name, video_name)

# check txt video num
with open(TRAIN_LSTM_FILE, 'r') as train_file:
    train_video = map(lambda x: x.split(' ')[0], train_file.readlines())
with open(TEST_LSTM_FILE, 'r') as test_file:
    test_video = map(lambda x: x.split(' ')[0], test_file.readlines())

video_list = []
video_list.extend(train_video)
video_list.extend(test_video)
if len(video_list) != len(video_in_db_list):
    print "Video num doesn't match."
'''

frame_list = []
for path in os.walk(CONV_FRAME_BK_PATH):
    if path[0] == CONV_FRAME_BK_PATH:
        continue
    frame_path_list = map(lambda x: os.path.join(path[0], x), path[2])
    frame_list.extend(frame_path_list)

for frame in frame_list:
    try:
        Image.open(frame)
    except:
        print "FRAME_PATH: ", frame
        traceback.print_exc()
