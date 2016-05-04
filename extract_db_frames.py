#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
import os
import sys
import threading
import pprint


DB_PATH = '/disk/zjingcong/frame_db/'

if len(sys.argv) == 2:
    DATASETPATH = sys.argv[1]   # DATASETPATH = '/disk/zjingcong/Smoke_Dataset_20160503/'
else:
    DATASETPATH = '/disk/zjingcong/Smoke_Dataset_20160503/'

mutex = threading.Lock()
success_num = 0
fail_num = 0
skip_num = 0
success_list = []
fail_list = []
skip_list = []


class extract_thread(threading.Thread):
    def __init__(self, video_path):
        super(extract_thread, self).__init__()
        # print "Extract video {0}...".format(video_path)
        self.video_path = video_path

    def run(self):
        global success_num, fail_num, fail_list, success_list
        success = True
        try:
            command = ['/bin/bash', 'extract_frames.sh', self.video_path, '30']
            p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            p.communicate()
            # print "Extract video {0} success.".format(self.video_path)
        except Exception, e:
            print "[ERROR] {0}: {1}".format(self.video_path, e)
            success = False

        if mutex.acquire():
            if success:
                success_num += 1
                success_list.append(self.video_path)
            else:
                fail_num += 1
                fail_list.append(self.video_path)

            mutex.release()


def main():
    global success_num, fail_num, fail_list, success_list, skip_num, skip_list
    video_name_list = []
    for path in os.walk(DB_PATH):
        if path[0] == DB_PATH:
            video_name_list = path[1]
            break

    for path in os.walk(DATASETPATH):
        if path[0] == DATASETPATH:
            continue
        video_list = path[2]
        for video in video_list:
            video_path = os.path.join(path[0], video)
            if video.endswith('.avi') or video.endswith('.mp4'):
                video_name = video[: -4]
            else:
                print "[ERROR] {0}: Plz input .avi or .mp4 video.".format(video)
                fail_num += 1
                fail_list.append(video_path)
                continue

            if video_name in video_name_list:
                print "Skip video {0}: video frame {0} exists.".format(video_name)
                skip_num += 1
                skip_list.append(video_path)
                continue

            # extract video frames
            video_extractor = extract_thread(video_path)
            video_extractor.start()

    while threading.activeCount() > 1:
        pass

    # extractor summary
    print '\n'
    print "========== Extractor Summary =========="
    print "Success videos: "
    pprint.pprint(success_list)
    print "Fail videos: "
    pprint.pprint(fail_list)
    print "Skip videos: "
    pprint.pprint(skip_list)
    print "Success videos: {0}".format(success_num)
    print "Fail videos: {0}".format(fail_num)
    print "Skip videos: {0}".format(skip_num)

if __name__ == '__main__':
    main()
