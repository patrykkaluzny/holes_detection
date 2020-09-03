import cv2 as cv
import numpy as np
import glob
import os
from matplotlib import pyplot as plt
from variables import block_colors, background_color, circle_param
from managing_data import get_images_from_path, get_path_args, get_entry_json, save_exit_jason, get_file_name_without_extension, check_for_redundand_block
from testing_functions import draw_contours_rectangles, testing_circles, testinng_circles_2
from blocks_recognition import detect_color, noise_remove_block, detect_circles
from image_partition import enlarge, get_objects_from_img, detect_block, noise_remove_img
import sys
import json
from circle_detection import detect_circle

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

# load entry json
entry_json = get_entry_json(entry_json_path)


results_dict = {}
for img, name in images_and_names:
    name = get_file_name_without_extension(name)
    blocks_results_list = []
    img_HSV = cv.cvtColor(img.copy(), cv.COLOR_BGR2HSV)
    img_threshold_background = cv.inRange(img_HSV, (background_color['min_hue'], background_color['min_sat'],
                                background_color['min_val']), (background_color['max_hue'], background_color['max_sat'],
                                background_color['max_val']))
    img_threshold_white = cv.inRange(img_HSV, (block_colors['white']['min_hue'], block_colors['white']['min_sat'],
                                block_colors['white']['min_val']), (block_colors['white']['max_hue'],
                                block_colors['white']['max_sat'], block_colors['white']['max_val']))
    img_threshold_background = cv.bitwise_not(img_threshold_background)
    img_threshold = cv.bitwise_or(img_threshold_white, img_threshold_background)
    img_threshold = cv.bitwise_not(img_threshold)
    img_threshold = enlarge(img_threshold, enlarge_size)

    filtered_img = noise_remove_img(img_threshold)

    detected_contours = detect_block(filtered_img)
    # draw_contours_rectangles(enlarge(img, enlarge_size), detected_contours)
    blocks = get_objects_from_img(enlarge(img_HSV.copy(), enlarge_size), detected_contours)


    for i,block in enumerate(blocks):
        # block_to_show = cv.cvtColor(block.copy(), cv.COLOR_HSV2BGR)
        results = {'red': '',
                   'blue': '',
                   'white': '',
                   'grey': '',
                   'yellow': '',
                   'result': ''}

        for key, color_value in block_colors.items():

            detected_color_contours = detect_color(block, color_value)
            results[key] = str(len(detected_color_contours))

        block = cv.cvtColor(block, cv.COLOR_HSV2BGR)
        block = cv.cvtColor(block, cv.COLOR_BGR2GRAY)
        number_of_circle = detect_circle(block)
        results['result'] = number_of_circle
        blocks_results_list.append(results)

    check_for_redundand_block(entry_json, blocks_results_list, name)
    results_dict[name] = blocks_results_list


save_exit_jason(entry_json, results_dict, exit_json_path)
cv.waitKey(0)
