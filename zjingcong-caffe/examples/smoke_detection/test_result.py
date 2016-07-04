#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Classify the whole test dataset and calculate the accuracy
# Usage: python test_result.py <test_file_path> <gpu_id> <lstm_caffemodel> <evaluation_mode>
# EX: test_file_path =
# '/home/zjc/workspace/backup/test_train_txtFile_backup/lstm-train-2016-05-22-20:05/Smoke_split_testVideo.txt'
# gpu_id = 0
# lstm_model = 'snapshots_lstm_RGB_iter_200.caffemodel'

from classify_video import videoClassifier

import pprint
import sys
import yaml

clip_length = 16
stride_length = 8

if len(sys.argv) > 3:
    test_file_path = sys.argv[1]
    gpu_id = int(sys.argv[2])
    lstm_model = sys.argv[3]
else:
    print "Check argv: [USAGE]python test_result.py <test_file_path> <gpu_id> <lstm_caffemodel>"
    sys.exit(1)

yaml_tmp_file = '/home/zjc/log/result_{0}.yaml'.format(lstm_model.split('.')[0])

# initialization
with open(yaml_tmp_file, 'a') as create_file:
    print "Create yaml file: ", yaml_tmp_file
yaml_file = file(yaml_tmp_file, 'r')
video_detected_list = yaml.load(yaml_file)
if type(video_detected_list) == list:
    videoname_detected_list = map(lambda x: x.get('name'), video_detected_list)
else:
    video_detected_list = []
    videoname_detected_list = []

print "Caffemodel Used: ", lstm_model


# video_info: <tuple>(<str>video_path, <int>label)
def evaluation(video_info):
    video_path = video_info[0]
    label = video_info[1]
    video_name = video_path.split('/')[-1]
    video_result, frame_predictions = videoClassifier(video_path, gpu_device=gpu_id, lstm_caffemodel=lstm_model)
    result_list = video_detected_list
    result_list.append({'name': video_name, 'label': label, 'f_p': frame_predictions})

    with open(yaml_tmp_file, 'w') as yaml_file:
        yaml_file.write(yaml.dump(result_list, default_flow_style=False))

with open(test_file_path, 'r') as test_file:
    test_info_list = test_file.readlines()
# test_info_list: <list>[<tuple>(<str>video_path, <int>label)]
test_info_list = map(lambda x: (x.split(' ')[0], int(x.split(' ')[1])), test_info_list)
# video detection: <list>[<tuple>(<str>video_path, <int>label)]
videoname_undetected_list = [i for i in test_info_list if i[0].split('/')[-1] not in videoname_detected_list]
print "Undetected Videos: ", len(videoname_undetected_list)

# evaluation_result: <list>
# [<tuple>(<str>video_name, <int>video_evaluation_result, <float>error_frame_rate, <list>error_frame_id)]
# video_evaluation_result - 1: correct, 0: error
map(evaluation, videoname_undetected_list)
