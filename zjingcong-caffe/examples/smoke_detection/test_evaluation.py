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

yaml_tmp_file = '/home/zjc/log/evaluation_tmp.yaml'

if len(sys.argv) > 3:
    test_file_path = sys.argv[1]
    gpu_id = sys.argv[2]
    lstm_model = sys.argv[3]
else:
    print "Check argv: [USAGE]python test_evaluation.py <test_file_path> <gpu_id> <lstm_caffemodel>"
    sys.exit(1)

yaml_file = file(yaml_tmp_file, 'r')
video_detected_list = yaml.load(yaml_file)
videoname_detected_list = map(lambda x: x.get('name'), video_detected_list)

with open(test_file_path, 'r') as test_file:
    test_info_list = test_file.readlines()

print "Caffemodel Used: ", lstm_model


# video_info: <tuple>(<str>video_path, <int>label)
def evaluation(video_info):
    video_path = video_info[0]
    label = video_info[1]
    video_name = video_path.split('/')[-1]
    # get video result
    video_result, frame_predictions = videoClassifier(video_path)
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
    error_frame_id_list = [frame_id for frame_id, frame_result in enumerate(classifier_result_list)
                           if frame_result != label]
    error_frame_rate = float(len(error_frame_id_list)) / len(classifier_result_list)

    result = (video_name, video_evluation, error_frame_rate, error_frame_id_list)
    # record the tmp result
    f = file(yaml_tmp_file, 'r')
    result_list = yaml.load(f)
    result_list.append({'name': video_name, 'v_result': video_evluation,
                        'f_error_rate': error_frame_rate, 'f_error_id': error_frame_id_list})
    with open(yaml_tmp_file, 'w') as yaml_file:
        yaml_file.write(yaml.dump(result_list, default_flow_style=False))

    # return <tuple>(<str>video_name, <int>video_evaluation_result, <float>error_frame_rate, <list>error_frame_id)
    return result


# evaluation_result:
# <dict>
# {'name': video_name, 'v_result': video_evluation, 'f_error_rate': error_frame_rate, 'f_error_id': error_frame_id_list}
def summary_frame_evaluation(evaluation_result):
    video_name = evaluation_result.get('name')
    error_frame_rate = evaluation_result.get('f_error_rate')
    error_frame_id_list = evaluation_result.get('f_error_id')
    print "{name} | Error Frame Rate: {rate}".format(name=video_name, rate=error_frame_rate)
    print "Error Frames ID: ", error_frame_id_list


# test_info_list: <list>[<tuple>(<str>video_path, <int>label)]
test_info_list = map(lambda x: (x.split(' ')[0], int(x.split(' ')[1])), test_info_list)

"""
# video detection
video_undetected_list = [i for i in test_info_list if i[0].split('/')[-1] not in videoname_detected_list]
print "Undetected Videos: ", len(video_undetected_list)
# evaluation_result: <list>
# [<tuple>(<str>video_name, <int>video_evaluation_result, <float>error_frame_rate, <list>error_frame_id)]
# video_evaluation_result - 1: correct, 0: error
evaluation_result = map(evaluation, video_undetected_list)
"""

# summary
f2 = file(yaml_tmp_file, 'r')
evaluation_result_total = yaml.load(f2)
map(summary_frame_evaluation, evaluation_result_total)

total_frame_num = 0
total_smoke_num = 0
total_no_smoke_num = 0
f_error2smoke = 0         # real is no smoke and detection result is smoke
f_error2no_smoke = 0      # real is smoke and detection result is no smoke
total_error_num = 0

smoke_video = 0
no_smoke_video = 0
total = 0
v_error2smoke = 0
v_error2no_smoke = 0
error_video = 0
for item in test_info_list:
    video_path = item[0]
    label = item[1]
    frame_num = len(glob.glob('%s/*.jpg' % video_path))
    tmp_list = [i for i in evaluation_result_total
                if i.get('name') == video_path.split('/')[-1]]
    if len(tmp_list) == 0:
        print "Didn't test ", video_path
        continue
    error_frame_num = len(tmp_list[0].get('f_error_id'))
    v_result = tmp_list[0].get('v_result')
    v_error = 0
    if v_result == 0:   # video result is false
        v_error = 1

    total_frame_num += frame_num
    total_error_num += error_frame_num
    total += 1
    error_video += v_error
    if label == 1:
        total_smoke_num += frame_num
        f_error2no_smoke += error_frame_num
        smoke_video += 1
        v_error2no_smoke += v_error
    else:
        total_no_smoke_num += frame_num
        f_error2smoke += error_frame_num
        no_smoke_video += 1
        v_error2smoke += v_error

print "total_frame_num", total_frame_num
print "total_smoke_num", total_smoke_num
print "total_no_smoke_num", total_no_smoke_num
print "f_error2smoke", f_error2smoke
print "f_error2no_smoke", f_error2no_smoke
print "total_error_num", total_error_num
print '=' * 20
print "total video", len(evaluation_result_total), total
print "smoke_video", smoke_video
print "no_smoke_video", no_smoke_video
print "v_error2smoke", v_error2smoke
print "v_error2no_smoke", v_error2no_smoke
print "error_video", error_video
