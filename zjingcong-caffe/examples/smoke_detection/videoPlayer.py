#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
import subprocess
import os
import logging
import sys
import time

mpg_path = '/disk/zjingcong/tmp/mpg_video'
frame_rate_path = '/disk/zjingcong/tmp/video_30_fps'
smoke_detection_fps = 30
clip_length = 16

frame_count = 0
frame_rate = 30
clock = pygame.time.Clock()

scripttime = time.strftime("%Y-%m-%d-%H:%M", time.localtime())


def cleaner():
    # rm mpg_video and fps_30_video
    command = ['rm', mpg_video_path, fps_30_video_path]
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    if err != '':
        logging.error(err)
        sys.exit(1)


def init(video_path):
    global video_name, fps_30_video_path, mpg_video_path, warning_logo
    # video pre-process
    video_name = video_path.split('/')[-1]
    fps_30_video_path = os.path.join(frame_rate_path, '{0}-{1}'.format(scripttime, video_name))
    mpg_video_path = os.path.join(mpg_path, '{0}-{1}'.format(scripttime, video_name.split('.')[0] + '.mpg'))

    # set video frame_rate to 30 fps
    logging.info("Set video {0} frame rate to 30 fps...".format(video_path))
    command = ['ffmpeg', '-i', video_path, '-r', '30', fps_30_video_path]
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        out, err = p.communicate()
        logging.info("Set video {0} frame rate to 30 fps success.".format(video_path))
    except:
        logging.exception("Set video to 30 fps error")

    # convert video to mpg format
    logging.info("Convert video {0} frame rate to mpg format...".format(fps_30_video_path))
    command = ['ffmpeg', '-i', fps_30_video_path,
               '-vcodec', 'mpeg1video', '-acodec', 'libmp3lame', '-intra', mpg_video_path]
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        out, err = p.communicate()
        logging.info("Convert video {0} to mpg format success.".format(video_path))
    except:
        logging.exception("Convert video to mpg format error")


def videoPlayer(video_path, smoke_list):
    # initialization
    init(video_path)
    global frame_count
    pygame.init()

    movie = pygame.movie.Movie(mpg_video_path)
    win_size = movie.get_size()

    screen = pygame.display.set_mode(win_size)
    movie_screen = pygame.Surface(movie.get_size()).convert()

    warning_logo = pygame.image.load('warning.PNG')
    scale = float((win_size[1] / 10)) / warning_logo.get_size()[1]
    warning_logo = pygame.transform.scale(warning_logo,
                                          (int(scale * warning_logo.get_size()[0]),
                                           int(scale * warning_logo.get_size()[1])))

    real_to_smoke = (frame_rate / smoke_detection_fps) * clip_length
    smoke_list_new = map(lambda x: [x] * real_to_smoke, smoke_list)
    smoke_frame_list = []
    for smoke_info in smoke_list_new:
        smoke_frame_list.extend(smoke_info)

    movie.set_display(movie_screen)
    movie.play()

    playing = True
    while playing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                movie.stop()
                playing = False

        screen.blit(movie_screen, (0, 0))
        if frame_count < len(smoke_frame_list):
            if smoke_frame_list[frame_count] == 1:
                screen.blit(warning_logo, (movie.get_size()[0] / 2 - warning_logo.get_size()[0] / 2, 5))

        frame_count += 1
        clock.tick(frame_rate)

        pygame.display.update()

    pygame.quit()

    # cleaner
    cleaner()

'''
# test
test_video = '/disk/zjingcong/testVideo/truck_fire_1_black_smoke.mp4'
smoke_list = [1, 0, 1, 1, 1, 1, 1, 0, 0, 0]
videoPlayer(test_video, smoke_list)
'''
