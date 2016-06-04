#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Classify the whole test dataset and calculate the accuracy
# Usage: python test_evaluation.py <test_file_path> <gpu_id> <lstm_caffemodel> <evaluation_mode>
# EX: test_file_path =
# '/home/zjc/workspace/backup/test_train_txtFile_backup/lstm-train-2016-05-22-20:05/Smoke_split_testVideo.txt'
# gpu_id = 0
# lstm_model = 'snapshots_lstm_RGB_iter_1600.caffemodel'

from classify_video import videoClassifier

import pprint
import sys
import glob
import numpy as np
import yaml

clip_length = 16
offset = 24
stride_length = 8

if len(sys.argv) > 3:
    test_file_path = sys.argv[1]
    gpu_id = int(sys.argv[2])
    lstm_model = sys.argv[3]
else:
    print "Check argv: [USAGE]python test_evaluation.py <test_file_path> <gpu_id> <lstm_caffemodel>"
    sys.exit(1)

yaml_tmp_file = '/home/zjc/log/evaluation_{0}.yaml'.format(lstm_model.split('.')[0])

with open(yaml_tmp_file, 'w') as create_file:
    print "Create yaml file: ", yaml_tmp_file
yaml_file = file(yaml_tmp_file, 'r')
video_detected_list = yaml.load(yaml_file)
if type(video_detected_list) == list:
    videoname_detected_list = map(lambda x: x.get('name'), video_detected_list)
else:
    video_detected_list = []
    videoname_detected_list = []

with open(test_file_path, 'r') as test_file:
    test_info_list = test_file.readlines()

print "Caffemodel Used: ", lstm_model


# video_info: <tuple>(<str>video_path, <int>label)
def evaluation(video_info):
    video_path = video_info[0]
    label = video_info[1]
    video_name = video_path.split('/')[-1]
    # get video result
    video_result, frame_predictions = videoClassifier(video_path, gpu_device=gpu_id, lstm_caffemodel=lstm_model)
    video_evluation = 0
    if video_result == label:
        video_evluation = 1

    # get frame result
    frame_num = len(glob.glob('%s/*.jpg' % video_path))
    index_list = []
    index = range(frame_num)
    for j in range(0, frame_num, stride_length):
        if (j + clip_length) < frame_num:
            index_list.extend(index[j: j + clip_length])
        else:
            index_list.extend(index[-clip_length:])

    tmp_list = list(frame_predictions)
    result_list = []
    classifier_result_list = []
    for frame_id in xrange(frame_num):
        frame_index_list = [k for k in xrange(len(index_list)) if index_list[k] == frame_id]
        frame_predictions_array = np.array(map(lambda x: tmp_list[x], frame_index_list))
        result_0 = np.mean(frame_predictions_array, 0)[0]
        result_1 = np.mean(frame_predictions_array, 0)[1]
        result_list.append((result_0, result_1))
        classifier_result_list.append(np.mean(frame_predictions_array, 0).argmax())

    print classifier_result_list
    error_frame_id_list = [frame_id for frame_id, frame_result in enumerate(classifier_result_list)
                           if frame_result != label]
    error_frame_rate = float(len(error_frame_id_list)) / len(classifier_result_list)

    result_list = video_detected_list
    result_list.append({'name': video_name, 'v_result': video_evluation, 'frame_num': frame_num,
                        'f_error_rate': error_frame_rate, 'f_error_id': error_frame_id_list})
    with open(yaml_tmp_file, 'w') as yaml_file:
        yaml_file.write(yaml.dump(result_list, default_flow_style=False))

# test_info_list: <list>[<tuple>(<str>video_path, <int>label)]
test_info_list = map(lambda x: (x.split(' ')[0], int(x.split(' ')[1])), test_info_list)

# video detection
video_undetected_list = [i for i in test_info_list if i[0].split('/')[-1] not in videoname_detected_list]
print "Undetected Videos: ", len(video_undetected_list)
# evaluation_result: <list>
# [<tuple>(<str>video_name, <int>video_evaluation_result, <float>error_frame_rate, <list>error_frame_id)]
# video_evaluation_result - 1: correct, 0: error
map(evaluation, video_undetected_list)
