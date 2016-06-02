#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Classify the whole test dataset and calculate the accuracy
# Usage: python test_evaluation.py <test_file_path> <gpu_id> <lstm_caffemodel> <evaluation_mode>

from classify_video import videoClassifier

import pprint
import sys
import glob
import numpy as np

'''
test_file_path = '/home/zjc/workspace/backup/test_train_txtFile_backup/' \
                 'lstm-train-2016-05-22-20:05/Smoke_split_testVideo.txt'
gpu_id = 0
lstm_model = 'snapshots_lstm_RGB_iter_1600.caffemodel'
'''

clip_length = 16
offset = 24
frame_rate = 15
stride_length = 8

if len(sys.argv) > 3:
    test_file_path = sys.argv[1]
    gpu_id = sys.argv[2]
    lstm_model = sys.argv[3]
else:
    print "Check argv: [USAGE]python test_evaluation.py <test_file_path> <gpu_id> <lstm_caffemodel>"
    sys.exit(1)

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

    # return <tuple>(<str>video_name, <int>video_evaluation_result, <float>error_frame_rate, <list>error_frame_id)
    return video_name, video_evluation, error_frame_rate, error_frame_id_list


# evaluation_result:
# <tuple>(<str>video_name, <int>video_evaluation_result, <float>error_frame_rate, <list>error_frame_id)
def summary_frame_evaluation(evaluation_result):
    video_name = evaluation_result[0]
    error_frame_rate = evaluation_result[2]
    error_frame_id_list = evaluation_result[3]
    print "{name} | Error Frame Rate: {rate}".format(name=video_name, rate=error_frame_rate)
    print "Error Frames ID: ", error_frame_id_list


# test_info_list: <list>[<tuple>(<str>video_path, <int>label)]
test_info_list = map(lambda x: (x.split(' ')[0], int(x.split(' ')[1])), test_info_list)
# evaluation_result: <list>
# [<tuple>(<str>video_name, <int>video_evaluation_result, <float>error_frame_rate, <list>error_frame_id)]
# video_evaluation_result - 1: correct, 0: error
evaluation_result = map(evaluation, test_info_list)

# frame summary
print "=================== Evaluation Video Frames Summary ==================="
map(summary_frame_evaluation, evaluation_result)

# video summary
correct = len([i for i in evaluation_result if i[1] == 1])
total = len(evaluation_result)
error = total - correct
error_video_list = [i[0] for i in evaluation_result if i[1] == 0]
correct_video_list = [i[0] for i in evaluation_result if i[1] == 1]
print "=================== Evaluation Videos Summary ==================="
print "# Total Videos: ", total
print "# Correct Videos: ", correct
print "# Error Videos: ", error
print "# Accuracy: ", float(correct) / total
print "# Correct Videos List: "
pprint.pprint(correct_video_list)
print "# Error Videos List: "
pprint.pprint(error_video_list)
