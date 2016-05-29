#!/usr/bin/env python
# -*- coding: utf-8 -*-

from classify_video import videoClassifier

import sys

if len(sys.argv) > 1:
    video_path = sys.argv[1]
else:
    video_path = '/disk/zjingcong/frame_db/factory_fire_5_black_smoke'

print videoClassifier(video_path)[0]
