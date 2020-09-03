import glob
import os
import cv2 as cv
import sys
import json


def get_images_from_path(img_dir_path):
    images_and_names = []
    try:
        for file in glob.glob(img_dir_path+'\\img_*.jpg'):
            img = cv.imread(file)
            img = cv.resize(img, None, fx=0.5, fy=0.5)
            name = os.path.basename(file)
            images_and_names.append((img, name))
    except (ValueError, Exception):
        print('error during loading images')
        sys.exit(0)
    return images_and_names


def get_path_args():
    img_dir_path, entry_json_path, exit_json_path = sys.argv[1:]
    return img_dir_path, entry_json_path, exit_json_path


def get_entry_json(entry_json_path):
    try:
        with open(entry_json_path) as json_file:
            entry_json = json.load(json_file)
    except (ValueError, Exception):
        print("entry json not loaded")
        sys.exit(0)
    return entry_json

def save_exit_jason(entry_json,result_json, exit_json_path):
    entry_json = prepare_entry_json(entry_json)
    entry_json = compare_detection_results(result_json, entry_json)
    exit_json = prepare_exit_json(entry_json)
    with open(exit_json_path, 'w') as outfile:
        json.dump(exit_json, outfile)


def prepare_entry_json(entry_json):
    for image_name, block_list in entry_json.items():
        for block in block_list:
            block['result'] = ''
    return entry_json

def compare_detection_results(detection_json, entry_json):
    for matching_blocks in range(5,-1,-1):
        for image_name, block_list in entry_json.items():
            for detection_image_name, detection_list in detection_json.items():
                if detection_image_name == image_name:
                    for block_result in detection_list:
                        if block_result['result'] != '':
                            for block in block_list:
                                if block['result'] == '':
                                    if compare_blocks(block, block_result,matching_blocks):
                                        block['result'] = block_result['result']
                                        block_result['result'] = ''
    return entry_json

def compare_blocks(block1, block2, number_of_correct_values):
    shared_items = {k: block1[k] for k in block1 if k in block2 and block1[k] == block2[k]}
    if len(shared_items) == number_of_correct_values:
        return True
    return False

def prepare_exit_json(entry_json):
    output = {}

    for image_name, image_list in entry_json.items():
        result_list = []
        for block in image_list:
            result_list.append(block['result'])
        output[image_name] = result_list

    return output

def get_file_name_without_extension(name_with_extension):
    return os.path.splitext(name_with_extension)[0]

def check_for_redundand_block(entry_json, block_list, image_name):
    while len(entry_json[image_name]) < len(block_list):
        id = 0
        min_result = 10000
        for i,block in enumerate(block_list):
            if min_result > block['result']:
                min_result = block['result']
                id = i
        block_list.pop(id)



