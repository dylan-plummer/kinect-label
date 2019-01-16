import cv2
import os
import sys
import csv
import argparse
import numpy as np

labeled_dir = 'labeled/'

with open('labels.csv') as csv_file, open('info.dat', mode='w') as info_file:
    file = list(csv.reader(csv_file))
    boxes = ''
    file_name = ''
    all_obstacles = False
    num_obstacles = 0
    for i in range(len(file)):
        row = file[i]
        num_obstacles += 1
        print(row)
        file_name = row[0]
        if i < len(file) - 1:
            if file[i + 1][0] != file_name:
                all_obstacles = True
        else:
            all_obstacles = True
        x = int(row[2])
        y = int(row[5])
        width = int(row[3]) - x
        height = int(row[4]) - y
        boxes += str(x) + ' ' + \
                 str(y) + ' ' + \
                 str(width) + ' ' + \
                 str(height) + '   '
        if all_obstacles:
            info_file.write(labeled_dir + file_name + '.png  ' + str(num_obstacles) + '  ' + boxes + '\n')
            boxes = ''
            num_obstacles = 0
            all_obstacles = False
