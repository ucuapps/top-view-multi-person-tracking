# This file is the utility that allows you to merge the data from dataset as in the video in the readme.md

import cv2
import numpy as np
import os

paths = [
    './data/1.mp4',
    './data/2.mp4',
    './data/3.mp4',
    './data/4.mp4',
    './data/5.mp4'
]

captures = [cv2.VideoCapture() for v in paths]

for i, capture in enumerate(captures):
    capture.open(paths[i])
    assert capture.isOpened()

im_width = int(captures[0].get(cv2.CAP_PROP_FRAME_WIDTH))
im_height = int(captures[0].get(cv2.CAP_PROP_FRAME_HEIGHT))

out_size = (im_width * 3, im_height * 2)

fourcc = cv2.VideoWriter_fourcc(*'MJPG')
out = cv2.VideoWriter(os.environ.get("OUT_PATH", 'out.avi'), fourcc, 20, out_size)

i = int(os.environ.get("NUMBER_OF_FRAMES_TO_MERGE", 1000))

while i >= 0:
    cam1, cam2, cam3, cam4, cam5 = [capture.retrieve()[1] for capture in captures if capture.grab()]
    shape1 = list(cam1.shape)
    shape1[1] = 160
    shape2 = list(cam1.shape)
    shape2[1] = 1280 - 160

    upper = np.hstack((np.zeros(shape1), cam4, cam5, np.zeros(shape2)))
    lower = np.hstack((cam1, cam2, cam3))

    merged_frame = np.vstack((upper, lower))
    out.write(np.uint8(merged_frame))

    if i % 100 == 0:
        print("Left to merge %d frames" % i)

    i -= 1

out.release()
