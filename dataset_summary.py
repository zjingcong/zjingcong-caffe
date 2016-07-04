#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Get dataset summary. Return a dict of dataset info like: <dict>{<class>: <tuple>(<int>video_num, <int>frame_num)}

import glob
import yaml
import pprint

label_file = 'label_video.yaml'
f = file(label_file, 'r')
video_info_list = yaml.load(f)

# dataset_dict: <dict>{<class>: <tuple>(<int>video_num, <int>frame_num)}
dataset_dict = dict()
for video_info in video_info_list:
    video_path = video_info.get('path')
    video_class = video_info.get('class')
    frame_num = len(glob.glob('%s/*.jpg' % video_path))

    if video_class not in dataset_dict:
        dataset_dict[video_class] = (1, frame_num)
    else:
        dataset_dict[video_class] = (dataset_dict[video_class][0] + 1, dataset_dict[video_class][1] + frame_num)

pprint.pprint(dataset_dict)
