#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Usage: Nothing to do. Plz ignore it.

import os
import subprocess
import pprint
import time

PATH = '/home/zjc/workspace/git/zjingcong-caffe/zjingcong-caffe/examples/LRCN_activity_recognition'
SNAPSHOTPATH = '/disk/zjingcong/caffemodel/snapshot'

file_list = []
for path in os.walk(PATH):
    if path[0] == PATH:
        file_list = path[2]
        break


def move_file(file_name):
    try:
        command = ['mv', os.path.join(PATH, file_name), os.path.join(SNAPSHOTPATH, file_name)]
        p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        print out, err
    except Exception, e:
        print "ERROR: ", e

snapshot_file = dict()
snapshot_file['caffemodel'] = []
snapshot_file['solverstate'] = []
for index, file_name in enumerate(file_list):
    if file_name.endswith('.caffemodel'):
        snapshot_file['caffemodel'].append(file_name)
    elif file_name.endswith('.solverstate'):
        snapshot_file['solverstate'].append(file_name)

if len(snapshot_file.get('caffemodel')) > 2:
    snapshot_file.get('caffemodel').sort(key=lambda x: int(x.split('.')[0].split('_')[4]))
    snapshot_file.get('solverstate').sort(key=lambda x: int(x.split('.')[0].split('_')[4]))
    for file_name in snapshot_file.get('caffemodel'):
        move_file(file_name)
    for file_name in snapshot_file.get('solverstate'):
        move_file(file_name)

print "========== Moving file at: {0} ==========".format(time.ctime())
pprint.pprint(snapshot_file.get('caffemodel'))
pprint.pprint(snapshot_file.get('solverstate'))
