import cv2 as cv
import numpy as np
import glob
import os
from matplotlib import pyplot as plt
from variables import block_colors, background_color, circle_param
from managing_data import get_images_from_path, get_path_args, get_entry_json, save_exit_jason
from testing_functions import draw_contours_rectangles, testing_circles, testinng_circles_2
from blocks_recognition import detect_color, noise_remove_block, detect_circles
from image_partition import enlarge, get_objects_from_img, detect_block, noise_remove_img
import sys
import json

# get necessary paths
if len(sys.argv) == 1:
    img_dir_path = 'D:\\Studia\\sisw_projekt\\blocks_and_holes_detection\\imgs'
    entry_json_path = 'D:\\Studia\\sisw_projekt\\blocks_and_holes_detection\\files\\public.json'
    exit_json_path ='D:\\Studia\\sisw_projekt\\blocks_and_holes_detection\\files\\output.json'
elif len(sys.argv) == 4:
    img_dir_path, entry_json_path, exit_json_path = get_path_args()
else:
    print('wrong arguments')
    sys.exit(0)


# variables used in program
enlarge_size = 100
window_img_name = 'img'

# load images
images_and_names = get_images_from_path(img_dir_path)


for img, name in images_and_names:

    img_HSV = cv.cvtColor(img.copy(), cv.COLOR_BGR2HSV)
    img_threshold = cv.inRange(img_HSV, (background_color['min_hue'], background_color['min_sat'],
                background_color['min_val']), (background_color['max_hue'], background_color['max_sat'],
                background_color['max_val']))
    img_threshold = enlarge(img_threshold, enlarge_size)
    filtered_img = noise_remove_img(img_threshold)

    detected_contours = detect_block(filtered_img)
    # draw_contours_rectangles(enlarge(img), detected_contours)
    blocks = get_objects_from_img(enlarge(img_HSV.copy(), enlarge_size), detected_contours)


    testinng_circles_2(blocks)
    # testing_circles(blocks[0])

    cv.waitKey(0)
    cv.destroyAllWindows()

cv.waitKey(0)