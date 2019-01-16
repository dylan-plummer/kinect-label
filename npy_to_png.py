import cv2
import os
import numpy as np


frames_dir = 'neg_npy/'
saved_dir = 'labeled_neg/'
frame_i = 0
for file in os.listdir(frames_dir):
    if file.endswith(".npy"):
        file_path = frames_dir + file
        print(file_path)
        img = np.uint8(np.load(file_path))
        cv2.imwrite(saved_dir + file[:-4] + '.png', img)