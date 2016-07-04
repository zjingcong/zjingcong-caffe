#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Usage: python test_result_evaluation.py <threshold>
# The default threshold is 0.5

import yaml
import glob
import numpy as np
import pprint
import os

video_frame_db = '/disk/zjingcong/frame_db'
clip_length = 16
stride_length = 8


def classifier(result_array, classifier_threshold):
    smoke_probability = result_array[1]
    if smoke_probability >= classifier_threshold:
        result = 1
    else:
        result = 0

    return result


# result_info: <dict>{'f_p': frame_predictions, 'label': label, 'name': video_name}
def evluation(result_info, threshold):
    global video_result_summary
    frame_predictions = result_info.get('f_p')
    label = result_info.get('label')
    video_name = result_info.get('name')

    # get video result
    video_result = classifier(np.mean(frame_predictions, 0), threshold)
    video_evluation = 0
    if video_result == label:
        video_evluation = 1

    # get frame result
    frame_num = len(glob.glob('%s/*.jpg' % os.path.join(video_frame_db, video_name)))
    index_list = []
    index = range(frame_num)
    for j in range(0, frame_num, stride_length):
        if (j + clip_length) < frame_num:
            index_list.extend(index[j: j + clip_length])
        else:
            index_list.extend(index[-clip_length:])

    tmp_list = list(frame_predictions)
    classifier_result_list = []
    for frame_id in xrange(frame_num):
        frame_index_list = [k for k in xrange(len(index_list)) if index_list[k] == frame_id]
        frame_predictions_array = np.array(map(lambda x: tmp_list[x], frame_index_list))
        classifier_result_list.append(classifier(np.mean(frame_predictions_array, 0), threshold))

    error_frame_id_list = [frame_id for frame_id, frame_result in enumerate(classifier_result_list)
                           if frame_result != label]
    error_frame_rate = float(len(error_frame_id_list)) / len(classifier_result_list)

    video_result_summary.append({'name': video_name, 'v_result': video_evluation, 'frame_num': frame_num,
                                 'f_error_rate': error_frame_rate, 'f_error_id': error_frame_id_list})


def result_evaluation(threshold, show_result=False):
    '''
    # iter = 200
    result_yaml_file = '/home/zjc/log/result_snapshots_lstm_RGB_iter_200.yaml'
    evaluation_yaml_file = '/home/zjc/log/threshold_evaluation/' \
                           'evaluation_snapshots_lstm_RGB_iter_200_threshold_{0}.yaml'.format(threshold)
    '''
    # iter = 300
    result_yaml_file = '/home/zjc/log/result_snapshots_lstm_RGB_iter_300.yaml'
    evaluation_yaml_file = '/home/zjc/log/threshold_evaluation/' \
                           'evaluation_snapshots_lstm_RGB_iter_300_threshold_{0}.yaml'.format(threshold)
    '''
    # iter = 400
    result_yaml_file = '/home/zjc/log/result_snapshots_lstm_RGB_iter_400.yaml'
    evaluation_yaml_file = '/home/zjc/log/threshold_evaluation/' \
                           'evaluation_snapshots_lstm_RGB_iter_400_threshold_{0}.yaml'.format(threshold)
    '''
    f = file(result_yaml_file, 'r')
    result_total = yaml.load(f)
    global video_result_summary
    video_result_summary = []
    for result_info in result_total:
        evluation(result_info, threshold)
    if show_result is True:
        pprint.pprint(video_result_summary)
    with open(evaluation_yaml_file, 'w') as evaluation_file:
        evaluation_file.write(yaml.dump(video_result_summary, default_flow_style=False))

# test
# result_evaluation(0.5)
