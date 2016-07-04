#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Usage: (plz run after test_result_evaluation.py) python evaluation_summary.py <threshold>
# The default threshold is 0.5

import yaml
import pprint

test_file_path = '/home/zjc/workspace/backup/test_train_txtFile_backup/' \
                 'lstm-train-2016-06-01-23:51/Smoke_split_testVideo.txt'
video_label_file = '/home/zjc/workspace/git/zjingcong-caffe/label_video.yaml'


def recall(error2smoke, error2no_smoke, smoke, no_smoke):
    return float(smoke - error2no_smoke) / smoke


def precision(error2smoke, error2no_smoke, smoke, no_smoke):
    if (error2smoke + (smoke - error2no_smoke)) != 0:
        return float(smoke - error2no_smoke) / (error2smoke + (smoke - error2no_smoke))
    else:
        return 1


def false_rate(error2smoke, error2no_smoke, smoke, no_smoke):
    return float(error2smoke) / no_smoke


def summary(threshold, show_result=False):
    # iter = 200
    evaluation_yaml_file = '/home/zjc/log/threshold_evaluation/' \
                           'evaluation_snapshots_lstm_RGB_iter_200_threshold_{0}.yaml'.format(threshold)
    # iter = 300
    # evaluation_yaml_file = '/home/zjc/log/threshold_evaluation/' \
    #                        'evaluation_snapshots_lstm_RGB_iter_300_threshold_{0}.yaml'.format(threshold)
    # iter = 400
    # evaluation_yaml_file = '/home/zjc/log/threshold_evaluation/' \
    #                        'evaluation_snapshots_lstm_RGB_iter_400_threshold_{0}.yaml'.format(threshold)

    f = file(evaluation_yaml_file, 'r')
    evaluation_result_total = yaml.load(f)

    # summary
    # frame evaluation summary
    total_frame_num = 0
    total_smoke_num = 0
    total_no_smoke_num = 0
    f_error2smoke = 0  # real is no smoke and detection result is smoke
    f_error2no_smoke = 0  # real is smoke and detection result is no smoke
    total_error_num = 0

    # video evaluation summary
    smoke_video = 0
    no_smoke_video = 0
    total = 0
    v_error2smoke = 0
    v_error2no_smoke = 0
    error_video = 0

    class_summary = dict()
    error_videoname_list = []

    with open(test_file_path, 'r') as test_file:
        test_info_list = test_file.readlines()
    # test_info_list: <list>[<tuple>(<str>video_path, <int>label)]
    test_info_list = map(lambda x: (x.split(' ')[0], int(x.split(' ')[1])), test_info_list)

    label_file = file(video_label_file, 'r')
    label_info_list = yaml.load(label_file)

    for item in test_info_list:
        video_path = item[0]
        label = item[1]
        video_name = video_path.split('/')[-1]
        video_class = [i.get('class') for i in label_info_list if i.get('path') == video_path][0]

        if video_class not in class_summary:
            class_summary[video_class] = {'f_num': 0, 'v_num': 0, 'f_error': 0, 'v_error': 0}

        tmp_list = [i for i in evaluation_result_total if i.get('name') == video_name]
        if len(tmp_list) == 0:
            if show_result is True:
                print "Didn't test ", video_path
            continue

        frame_num = tmp_list[0].get('frame_num')
        error_frame_num = len(tmp_list[0].get('f_error_id'))
        v_result = tmp_list[0].get('v_result')
        v_error = 0
        if v_result == 0:  # video result is false
            v_error = 1
            error_videoname_list.append((video_class, video_name))

        total_frame_num += frame_num
        total_error_num += error_frame_num
        total += 1
        error_video += v_error

        class_summary[video_class]['f_num'] += frame_num
        class_summary[video_class]['v_num'] += 1
        class_summary[video_class]['f_error'] += error_frame_num
        class_summary[video_class]['v_error'] += v_error

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

    # calculate video
    v_precision = precision(v_error2smoke, v_error2no_smoke, smoke_video, no_smoke_video)
    v_recall = recall(v_error2smoke, v_error2no_smoke, smoke_video, no_smoke_video)
    v_false_rate = false_rate(v_error2smoke, v_error2no_smoke, smoke_video, no_smoke_video)
    # calculate frame
    f_precision = precision(f_error2smoke, f_error2no_smoke, total_smoke_num, total_no_smoke_num)
    f_recall = recall(f_error2smoke, f_error2no_smoke, total_smoke_num, total_no_smoke_num)
    f_false_rate = false_rate(f_error2smoke, f_error2no_smoke, total_smoke_num, total_no_smoke_num)

    if show_result is True:
        print "Summary threshold: {0}".format(threshold)
        print '=' * 20
        print "total_frame_num", total_frame_num
        print "total_smoke_num", total_smoke_num
        print "total_no_smoke_num", total_no_smoke_num
        print "f_error2smoke", f_error2smoke
        print "f_error2no_smoke", f_error2no_smoke
        print "total_error_num", total_error_num
        print "f_precision", f_precision
        print "f_recall", f_recall
        print "f_false_rate", f_false_rate
        print '=' * 20
        print "total video", len(evaluation_result_total), total
        print "smoke_video", smoke_video
        print "no_smoke_video", no_smoke_video
        print "v_error2smoke", v_error2smoke
        print "v_error2no_smoke", v_error2no_smoke
        print "error_video", error_video
        print "v_precision", v_precision
        print "v_recall", v_recall
        print "v_false_rate", v_false_rate
        print '=' * 20
        print "Class Summary: "
        pprint.pprint(class_summary)
        print "Video Error: "
        pprint.pprint(error_videoname_list)

    return v_precision, v_recall, v_false_rate, f_precision, f_recall, f_false_rate

# summary single threshold
summary(0.5, show_result=True)
