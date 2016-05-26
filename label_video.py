#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Usage: python label_video <mode>(add conv-mirror)
# Default mode is to label original videos
# Mode: default/mirror

import os
import yaml
import random
import sys
import pprint

DATASETPATH = '/disk/zjingcong/Smoke_Dataset/'
LABELFILE = 'label_video.yaml'
DB_PATH = '/disk/zjingcong/frame_db/'

video_label_list = []

mode = 'default'
if len(sys.argv) > 1:
    if sys.argv[1] == 'mirror':
        mode = 'mirror'


# get conv pic list
video_name_list = []
for path in os.walk(DB_PATH):
    if path[0] == DB_PATH:
        video_name_list = path[1]
conv_video_name_list = [i for i in video_name_list if i.startswith('conv-')]


# label videos per sub dataset
def label_db(dataset_path):
    # parse db
    label_list = []
    for path in os.walk(dataset_path):
        if path[0] == dataset_path:
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
            video_name = video[: -4]
            video_frame_path = os.path.join(DB_PATH, video_name)
            label_list.append({'class': data_class, 'path': video_frame_path, 'label': label})
            # add mirror pic label
            if mode == 'mirror':
                mirror_video_name = 'conv-mirror-{0}'.format(video_name)
                if mirror_video_name in conv_video_name_list:
                    mirror_video_frame_path = os.path.join(DB_PATH, mirror_video_name)
                    label_list.append({'class': data_class, 'path': mirror_video_frame_path, 'label': label})

    print "Summary {0} videos in {1}. [{2} MODE]".format(len(label_list), dataset_path, mode)
    global video_label_list
    video_label_list += label_list

sub_dataset_list = []
for path in os.walk(DATASETPATH):
    if path[0] == DATASETPATH:
        sub_dataset_list = path[1]
        break

for dataset_name in sub_dataset_list:
    dataset_path = os.path.join(DATASETPATH, dataset_name)
    label_db(dataset_path)

# mis order label list
random.shuffle(video_label_list)

# write label_video file
# video class + video frame path + label
with open(LABELFILE, 'w') as label_file:
     label_file.write(yaml.dump(video_label_list, default_flow_style=False))

print "========== Total Dataset Summary =========="
print "# Total: {0}".format(len(video_label_list))
smoke_list = [i for i in video_label_list if i.get('label') == 1]
print "# Smoke videos: {0}".format(len(smoke_list))
print "# No smoke videos: {0}".format(len(video_label_list) - len(smoke_list))
