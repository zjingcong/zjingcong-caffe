#!/usr/bin/env python
# -*- coding: utf-8 -*-

import glob

test_file = 'Smoke_split_testVideo.txt'
train_file = 'Smoke_split_trainVideo.txt'


def summary(file_name):
    def get_frame_num(info):
        video_path = info[0]
        frame_num = len(glob.glob('%s/*.jpg' % video_path))
        return frame_num

    with open(file_name, 'r') as f:
        info_list = f.readlines()

    info_list = map(lambda x: (x.split(' ')[0], int(x.split(' ')[1])), info_list)
    smoke_list = [i for i in info_list if i[1] == 1]
    no_smoke_list = [i for i in info_list if i[1] == 0]

    smoke_num = len(smoke_list)
    no_smoke_num = len(info_list) - smoke_num
    smoke_frame = sum(map(get_frame_num, smoke_list))
    no_smoke_frame = sum(map(get_frame_num, no_smoke_list))

    print "{0} summary: ".format(file_name)
    print "# Smoke Videos: ", smoke_num
    print "# No Smoke Videos: ", no_smoke_num
    print "# Smoke Frames: ", smoke_frame
    print "# No Smoke Frames: ", no_smoke_frame
    print "# Total Videos: ", smoke_num + no_smoke_num
    print "# Total Frames: ", smoke_frame + no_smoke_frame

summary(train_file)
summary(test_file)
