#!/usr/bin/env python
# -*- coding: utf-8 -*-
# classify_video.py will classify a video using LRCN RGB model

import numpy as np
import glob
import sys

caffe_root = '../../'
sys.path.insert(0, caffe_root + 'python')
import caffe

CLIP_LENGTH = 16


# Initialize transformers
def initialize_transformer(image_mean, is_flow):
    shape = (10 * 16, 3, 227, 227)
    transformer = caffe.io.Transformer({'data': shape})
    channel_mean = np.zeros((3, 227, 227))
    for channel_index, mean_val in enumerate(image_mean):
        channel_mean[channel_index, ...] = mean_val
        transformer.set_mean('data', channel_mean)
        transformer.set_raw_scale('data', 255)
        transformer.set_channel_swap('data', (2, 1, 0))
        transformer.set_transpose('data', (2, 0, 1))
        transformer.set_is_flow('data', is_flow)

    return transformer


# classify video with LRCN model
def LRCN_classify_video(frames, net, transformer, is_flow):
    clip_length = CLIP_LENGTH
    offset = 8
    input_images = []
    for im in frames:
        input_im = caffe.io.load_image(im)
        if input_im.shape[0] < 240:
            input_im = caffe.io.resize_image(input_im, (240, 320))
        input_images.append(input_im)
    vid_length = len(input_images)
    input_data = []
    for i in range(0, vid_length, offset):
        if (i + clip_length) < vid_length:
            input_data.extend(input_images[i: i + clip_length])
        else:
            input_data.extend(input_images[-clip_length:])      # video may not be divisible by clip_length
    output_predictions = np.zeros((len(input_data), 2))

    for i in range(0, len(input_data), clip_length):
        clip_input = input_data[i: i + clip_length]
        clip_input = caffe.io.oversample(clip_input, [227, 227])
        clip_clip_markers = np.ones((clip_input.shape[0], 1, 1, 1))
        clip_clip_markers[0: 10, :, :, :] = 0
        caffe_in = np.zeros(np.array(clip_input.shape)[[0, 3, 1, 2]], dtype=np.float32)
        for ix, inputs in enumerate(clip_input):
            caffe_in[ix] = transformer.preprocess('data', inputs)
        out = net.forward_all(data=caffe_in, clip_markers=np.array(clip_clip_markers))
        output_predictions[i:i + clip_length] = np.mean(out['probs'], 1)

    return np.mean(output_predictions, 0).argmax(), output_predictions


# classify video with singleFrame model
def singleFrame_classify_video(frames, net, transformer, is_flow):
    batch_size = 16
    input_images = []
    for im in frames:
        input_im = caffe.io.load_image(im)
        if input_im.shape[0] < 240:
            input_im = caffe.io.resize_image(input_im, (240, 320))
        input_images.append(input_im)
    vid_length = len(input_images)

    output_predictions = np.zeros((len(input_images), 2))
    for i in range(0, len(input_images), batch_size):
        clip_input = input_images[i:min(i+batch_size, len(input_images))]
        clip_input = caffe.io.oversample(clip_input, [227, 227])
        clip_clip_markers = np.ones((clip_input.shape[0], 1, 1, 1))
        clip_clip_markers[0: 10, :, :, :] = 0
        if is_flow:  # need to negate the values when mirroring
            clip_input[5:, :, :, 0] = 1 - clip_input[5:, :, :, 0]
        caffe_in = np.zeros(np.array(clip_input.shape)[[0, 3, 1, 2]], dtype=np.float32)
        for ix, inputs in enumerate(clip_input):
            caffe_in[ix] = transformer.preprocess('data', inputs)
        net.blobs['data'].reshape(caffe_in.shape[0], caffe_in.shape[1], caffe_in.shape[2], caffe_in.shape[3])
        out = net.forward_all(data=caffe_in)
        output_predictions[i: i + batch_size] = np.mean(out['probs'].reshape(10, caffe_in.shape[0]/10, 2), 0)

    return np.mean(output_predictions, 0).argmax(), output_predictions


# Model fusion
def compute_fusion(RGB_pred, flow_pred, p):
    return np.argmax(p * np.mean(RGB_pred, 0) + (1-p) * np.mean(flow_pred, 0))


# mode: 1 - LSTM only, 2 - singleFrame only
def videoClassifier(video_frame_path, gpu_device=0, mode=1):
    # Initialization
    caffe.set_mode_gpu()
    caffe.set_device(gpu_device)

    smoke_mean_RGB = np.zeros((3, 1, 1))
    smoke_mean_RGB[0, :, :] = 103.939
    smoke_mean_RGB[1, :, :] = 116.779
    smoke_mean_RGB[2, :, :] = 128.68
    transformer_RGB = initialize_transformer(smoke_mean_RGB, False)

    # Extract list of frames in video
    RGB_frames = glob.glob('%s/*.jpg' % video_frame_path)

    # Models and weights
    lstm_model = 'deploy_lstm.prototxt'
    singleFrame_model = 'deploy_singleFrame.prototxt'
    RGB_lstm = 'snapshots_lstm_RGB_iter_1600.caffemodel'
    RGB_singleFrame = 'snapshots_singleFrame_RGB_iter_5000.caffemodel'

    if mode == 1:
        RGB_lstm_net = caffe.Net(lstm_model, RGB_lstm, caffe.TEST)
        # predictions_RGB_LRCN: a list of classified results for every clip
        class_RGB_LRCN, predictions_RGB_LRCN = LRCN_classify_video(RGB_frames, RGB_lstm_net, transformer_RGB, False)
        del RGB_lstm_net

        return class_RGB_LRCN, predictions_RGB_LRCN

    if mode == 2:
        RGB_singleFrame_net = caffe.Net(singleFrame_model, RGB_singleFrame, caffe.TEST)
        class_RGB_singleFrame, predictions_RGB_singleFrame = singleFrame_classify_video(RGB_frames, RGB_singleFrame_net,
                                                                                    transformer_RGB, False)
        del RGB_singleFrame_net

        return class_RGB_singleFrame, predictions_RGB_singleFrame
