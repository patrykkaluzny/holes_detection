import cv2 as cv
import numpy as np


def noise_remove_block(block):
    kernel = np.ones((3, 3), np.uint8)
    erode = cv.erode(block, kernel, iterations=2)
    kernel = np.ones((5, 5), np.uint8)
    dilate = cv.dilate(erode, kernel, iterations=5)
    return dilate


def detect_color(block_hsv, color):
    block_threshold = cv.inRange(block_hsv, (color['min_hue'], color['min_sat'], color['min_val']),
                                 (color['max_hue'], color['max_sat'], color['max_val']))
    # cv.imshow('thresh', block_threshold)
    block_filtered = noise_remove_block(block_threshold)
    # cv.imshow('filter', block_filtered)
    contours = find_color_contours(block_filtered)
    return contours



def find_color_contours(thresh):
    contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
    filtered_contures = []
    for contour in contours:
        hull = cv.convexHull(contour)
        area = cv.contourArea(hull)

        if area > 4000:

            filtered_contures.append(contour)
    return filtered_contures

def detect_circles(block, circle_param):
    block_grey = cv.cvtColor(block, cv.COLOR_BGR2grey)
    circles = cv.HoughCircles(block_grey, cv.HOUGH_GRADIENT, circle_param['dp'], circle_param['min_d'],
                              param1=circle_param['high_t'], param2=circle_param['low_t'],
                              minRadius=circle_param['min_r'], maxRadius=circle_param['max_r'])
    circles = np.uint16(np.around(circles))
    circles = np.uint16(np.around(circles))
    for i in circles[0, :]:
        # draw the outer circle
        cv.circle(block_grey, (i[0], i[1]), i[2], (0, 255, 0), 1)
    cv.imshow('block', block_grey)
    cv.waitKey(0)