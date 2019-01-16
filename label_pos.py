import cv2
import os
import sys
import csv
import argparse
import numpy as np


unlabeled_dir = 'unlabeled/'
labeled_dir = 'pos_npy/'

# initialize the list of reference points and boolean indicating
# whether cropping is being performed or not
obstacles = []
refPt = []
cropping = False
img = []


def get_frame_num():
    with open('labels.csv') as csv_file:
        max = 0
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


def click_and_crop(event, x, y, flags, param):
    # grab references to the global variables
    global refPt, cropping, img, obstacles

    # if the left mouse button was clicked, record the starting
    # (x, y) coordinates and indicate that cropping is being
    # performed
    if event == cv2.EVENT_LBUTTONDOWN:
        refPt = [(x, y)]
        cropping = True

    # check to see if the left mouse button was released
    elif event == cv2.EVENT_LBUTTONUP:
        # record the ending (x, y) coordinates and indicate that
        # the cropping operation is finished
        refPt.append((x, y))
        cropping = False
        obstacles.append(refPt)
        # draw a rectangle around the region of interest
        cv2.rectangle(img, refPt[0], refPt[1], (0, 255, 0), 2)
        cv2.imshow("image", img)


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
            img = cv2.cvtColor(np.uint8(img), cv2.COLOR_GRAY2BGR)
            cv2.namedWindow("image")
            cv2.setMouseCallback("image", click_and_crop)

            # keep looping until the 'q' key is pressed
            while True:
                # display the image and wait for a keypress
                cv2.imshow("image", img)
                key = cv2.waitKey(1) & 0xFF

                # if the 'r' key is pressed, reset the cropping region
                if key == ord("r"):
                    img = clone.copy()
                    obstacles = []

                # if the 's' key is pressed, save the labels if there are any and move the image from unlabeled
                # to labeled directory
                elif key == ord("s"):
                    if len(obstacles) > 0:
                        save_labels(clone, obstacles, frame_i)
                        frame_i += 1
                        obstacles = []
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
