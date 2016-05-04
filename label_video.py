#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

DATASETPATH = sys.argv[1]   # DATASETPATH = '/disk/zjingcong/Smoke_Dataset_20160503/'
LABELFILE = 'label_video.txt'
DB_PATH = '/disk/zjingcong/frame_db/'

# parse db
label_list = []
for path in os.walk(DATASETPATH):
    if path[0] == DATASETPATH:
        continue
    data_class = path[0].split('/')[-1]
    video_list = path[2]

    # label 0: no smoke
    # label 1: smoke
    if 'smoke' not in data_class:
        label = 0
    else:
        label = 1

    for video in video_list:
        video_name = video.strip('.mp4')
        video_name = video_name.strip('.avi')
        video_frame_path = os.path.join(DB_PATH, video_name)
        label_list.append('{0} {1}\n'.format(video_frame_path, label))

print "Summary {0} videos.".format(len(label_list))

# update label_video file
with open(LABELFILE, 'r') as label_file:
    video_data = label_file.readlines()
label_list = label_list + video_data
label_list = list(set(label_list))
label_str = ''.join(map(str, label_list))

with open(LABELFILE, 'w') as label_file:
    label_file.write(label_str)

