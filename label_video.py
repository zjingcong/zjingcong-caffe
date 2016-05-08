#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import yaml


DATASETPATH = '/disk/zjingcong/Smoke_Dataset/'
LABELFILE = 'label_video.yaml'
DB_PATH = '/disk/zjingcong/frame_db/'

video_label_list = []


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

    print "Summary {0} videos in {1}.".format(len(label_list), dataset_path)
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

# write label_video file
# video class + video frame path + label
with open(LABELFILE, 'w') as label_file:
    label_file.write(yaml.dump(video_label_list, default_flow_style=False))

print "========== Total Dataset Summary =========="
print "# Total: {0}".format(len(video_label_list))
smoke_list = [i for i in video_label_list if i.get('label') == 1]
print "# Smoke videos: {0}".format(len(smoke_list))
print "# No smoke videos: {0}".format(len(video_label_list) - len(smoke_list))
