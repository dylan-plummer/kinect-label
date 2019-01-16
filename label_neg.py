import cv2
import os
import sys
import csv
import argparse
import numpy as np


unlabeled_dir = 'unlabeled_neg/'
labeled_dir = 'neg_npy/'

cropping = False
img = []


def get_frame_num():
    with open('info.dat', mode='ab+') as file:
        file_name = file.readlines()[-1].decode().split(' ')[0]
        print(file_name)
        max = int(file_name[file_name.index('/') + 1:file_name.index('.')])
    with open('labels.csv') as csv_file:
        file = list(csv.reader(csv_file))
        for row in file[1:]:
            if int(row[0]) > max:
                max = int(row[0])
        return max


def save_labels(img, obstacles, frame_num):
    with open('labels.csv', mode='ab') as csv_file:
        writer = csv.writer(csv_file)
        id = 1
        for obstacle in obstacles:
            #filename, id, x_min, x_max, y_min, y_max
            row = [frame_num, id, obstacle[0][0], obstacle[1][0], obstacle[0][1], obstacle[1][1]]
            id += 1
            print('Adding label', row)
            writer.writerow(row)
        np.save(labeled_dir + str(frame_num) + '.npy', img)


def label_images(max_frame=0):
    global img, obstacles
    frame_i = max_frame + 1
    for file in os.listdir(unlabeled_dir):
        filename = file
        if filename.endswith(".npy"):
            file_path = unlabeled_dir + filename
            print(file_path)
            img = np.load(file_path)
            clone = img.copy()
            cv2.namedWindow("image")

            # keep looping until the 'q' key is pressed
            while True:
                # display the image and wait for a keypress
                cv2.imshow("image", img)
                key = cv2.waitKey(1) & 0xFF

                # if the 's' key is pressed, save the labels if there are any and move the image from unlabeled
                # to labeled directory
                if key == ord("s"):
                    with open('info.dat', 'ab') as info_file:
                        np.save(labeled_dir + str(frame_i) + '.npy', img)
                        info_file.write(labeled_dir + str(frame_i) + '.npy  0' + '\n')
                        frame_i += 1
                    os.remove(file_path)
                    break

                elif key == ord('n'):
                    os.remove(file_path)
                    break

                elif key == ord('q'):
                    cv2.destroyAllWindows()
                    sys.exit(0)

            # close all open windows
            cv2.destroyAllWindows()


max_frame = get_frame_num()
print(max_frame)
label_images(max_frame=max_frame)