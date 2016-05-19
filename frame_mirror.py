#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Image
import os
import ImageOps
import subprocess
import threading
import traceback
import time


FRAME_DB_PATH = '/disk/zjingcong/frame_db'


class mirrorPicThread(threading.Thread):
    def __init__(self, thread_id, video_frame_path):
        self.thread_id = thread_id
        self.video_frame_path = video_frame_path
        super(mirrorPicThread, self).__init__()
        print "Thread {0} - Mirror frames in {1}...".format(self.thread_id, self.video_frame_path)
        self.start_time = time.time()

    @staticmethod
    def _mirror_pic(pic_path):
        pic_name = os.path.split(pic_path)[1]
        video_name = os.path.split(pic_path)[0].split('/')[-1]
        mirror_pic_name = 'conv-mirror-{0}'.format(pic_name)
        mirror_pic_path = os.path.join(FRAME_DB_PATH, 'conv-mirror-{0}'.format(video_name))
        command = ['mkdir', '-m', '775', mirror_pic_path]
        p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p.communicate()

        img = Image.open(pic_path)
        img_mirror = ImageOps.mirror(img)
        img_mirror.save(os.path.join(mirror_pic_path, mirror_pic_name))

    def run(self):
        try:
            frame_list = []
            for path in os.walk(self.video_frame_path):
                if path[0] == self.video_frame_path:
                    frame_list = path[2]
                    break
            frame_list = map(lambda x: os.path.join(self.video_frame_path, x), frame_list)
            for frame_path in frame_list:
                self._mirror_pic(frame_path)
            print "Thread {0} complete. Time Usage: {1}".format(self.thread_id, time.time() - self.start_time)
        except:
            print "Thread {0} fail. Time Usage: {1}".format(self.thread_id, time.time() - self.start_time)
            traceback.print_exc()


def main():
    # get all the video name in the frame_db dir
    video_frame_path_list = []
    for path in os.walk(FRAME_DB_PATH):
        if path[0] == FRAME_DB_PATH:
            video_frame_path_list = path[1]
            break

    # list video name for videos that already been mirrored
    mirror_list = [i for i in video_frame_path_list if i.startswith('conv-mirror-')]
    mirror_list = map(lambda x: x[12:], mirror_list)

    # filter video with mirror_conv
    video_frame_path_list = [i for i in video_frame_path_list
                             if i.startswith('conv-') is False and i not in mirror_list]
    video_frame_path_list = map(lambda x: os.path.join(FRAME_DB_PATH, x), video_frame_path_list)

    # start mirror threads
    for index, video_frame_path in enumerate(video_frame_path_list):
        mirror_thread = mirrorPicThread(index, video_frame_path)
        mirror_thread.start()

    while threading.activeCount() > 1:
        pass

    print "=============== Mirror Summary ==============="
    print "Mirror Complete. Mirror {0} videos.".format(len(video_frame_path_list))

if __name__ == '__main__':
    main()
