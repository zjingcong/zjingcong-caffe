# classify_video.py will classify a video using LRCN RGB model
# Use: classify_video.py video, where video is the video you wish to classify.
# If no video is specified, the video "outdoor_fire_1_black_smoke" will be classified.

import numpy as np
import glob
import sys

caffe_root = '../../'
sys.path.insert(0, caffe_root + 'python')
import caffe

caffe.set_mode_gpu()
caffe.set_device(0)

caffemodel_path = '/home/zjc/zjingcong-caffe/zjingcong-caffe/examples/LRCN_activity_recognition'


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
    clip_length = 16
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
        else:  # video may not be divisible by clip_length
            input_data.extend(input_images[-clip_length:])
    output_predictions = np.zeros((len(input_data), 2))

    for i in range(0, len(input_data), clip_length):
        clip_input = input_data[i:i+clip_length]
        clip_input = caffe.io.oversample(clip_input, [227, 227])
        clip_clip_markers = np.ones((clip_input.shape[0], 1, 1, 1))
        clip_clip_markers[0: 10, :, :, :] = 0
        caffe_in = np.zeros(np.array(clip_input.shape)[[0, 3, 1, 2]], dtype=np.float32)
        for ix, inputs in enumerate(clip_input):
            caffe_in[ix] = transformer.preprocess('data', inputs)
        out = net.forward_all(data=caffe_in, clip_markers=np.array(clip_clip_markers))
        output_predictions[i:i + clip_length] = np.mean(out['probs'], 1)

    return np.mean(output_predictions, 0).argmax(), output_predictions


# Model fusion
def compute_fusion(RGB_pred, flow_pred, p):
    return np.argmax(p*np.mean(RGB_pred, 0) + (1-p)*np.mean(flow_pred, 0))


def videoClassifier(video_path):
    # Initialization
    smoke_mean_RGB = np.zeros((3, 1, 1))
    smoke_mean_RGB[0, :, :] = 103.939
    smoke_mean_RGB[1, :, :] = 116.779
    smoke_mean_RGB[2, :, :] = 128.68
    transformer_RGB = initialize_transformer(smoke_mean_RGB, False)

    # Extract list of frames in video
    RGB_frames = glob.glob('%s/*.jpg' % video_path)

    # Models and weights
    lstm_model = 'deploy_lstm.prototxt'
    RGB_lstm = 'snapshots_lstm_RGB_iter_2560.caffemodel'
    RGB_lstm_net = caffe.Net(lstm_model, RGB_lstm, caffe.TEST)
    class_RGB_LRCN, predictions_RGB_LRCN = LRCN_classify_video(RGB_frames, RGB_lstm_net, transformer_RGB, False)

    del RGB_lstm_net

    # Video Classifier
    video_classifier = {0: 'No_Smoke', 1: 'Smoke'}
    print "RGB LRCN model classified video as: %s.\n" % (video_classifier[class_RGB_LRCN])

'''
# test
if __name__ == '__main__':
    videoClassifier('waterfall_2')
'''
