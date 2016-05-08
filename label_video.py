#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import yaml
import subprocess


if len(sys.argv) == 2:
    DATASETPATH = sys.argv[1]   # DATASETPATH = '/disk/zjingcong/Smoke_Dataset_20160503/'
else:
    DATASETPATH = '/disk/zjingcong/Smoke_Dataset_20160503/'

LABELFILE = 'label_video.yaml'
DB_PATH = '/disk/zjingcong/frame_db/'

command = ['touch', LABELFILE]
p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
out, err = p.communicate()
print out, err

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
        video_name = video[: -4]
        video_frame_path = os.path.join(DB_PATH, video_name)
        label_list.append({'class': data_class, 'path': video_frame_path, 'label': label})

print "Summary {0} videos.".format(len(label_list))

# update label_video file
# video class + video frame path + label
f = file(LABELFILE, 'r')
video_list = yaml.load(f)
if video_list is not None:
    label_list = video_list + label_list

with open(LABELFILE, 'w') as label_file:
    label_file.write(yaml.dump(label_list, default_flow_style=False))

print "========== Total Dataset Summary =========="
print "# Total: {0}".format(len(label_list))
smoke_list = [i for i in label_list if i.get('label') == 1]
print "# Smoke videos: {0}".format(len(smoke_list))
print "# No smoke videos: {0}".format(len(label_list) - len(smoke_list))
