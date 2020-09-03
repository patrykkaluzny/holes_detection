import cv2 as cv
import numpy as np
from variables import circle_param


def draw_contours_rectangles(img_to_draw, contours):
    for contour in contours[1:]:
        rect = cv.minAreaRect(contour)
        box = cv.boxPoints(rect)
        box = np.int0(box)
        img_to_draw = cv.drawContours(img_to_draw, [box], 0, (0, 0, 255), 4)

    # plt.imshow(img_to_draw, 'grey')
    # plt.show()
    cv.imshow('image', cv.resize(img_to_draw, None, fx=0.5, fy=0.5))
    cv.waitKey(0)


def empty_callback(value):
    pass


def testing_circles(block):
    window_name = 'block_circle'
    cv.namedWindow(window_name)
    cv.createTrackbar('Threshold_high', window_name, circle_param['high_t'], 255, empty_callback)
    cv.createTrackbar('Threshold_low', window_name, circle_param['low_t'], 255, empty_callback)
    cv.createTrackbar('maxR', window_name, circle_param['max_r'], 400, empty_callback)
    cv.createTrackbar('minR', window_name, circle_param['min_r'], 250, empty_callback)
    cv.createTrackbar('minDist', window_name, circle_param['min_d'], 250, empty_callback)
    block_grey = cv.cvtColor(block, cv.COLOR_BGR2GRAY)
    while True:
        Threshold_high = cv.getTrackbarPos('Threshold_high', window_name)
        Threshold_low = cv.getTrackbarPos('Threshold_low', window_name)
        maxR = cv.getTrackbarPos('maxR', window_name)
        minR = cv.getTrackbarPos('minR', window_name)
        minDist = cv.getTrackbarPos('minDist', window_name)

        circles = cv.HoughCircles(block_grey, cv.HOUGH_GRADIENT, 1, minDist, param1=Threshold_high,
                                  param2=Threshold_low, minRadius=minR, maxRadius=maxR)
        block_to_draw = block.copy()
        if circles is not None:
            print(len(circles))
            circles = np.uint16(np.around(circles))
            for i in circles[0, :]:
                # draw the outer circle
                cv.circle(block_to_draw, (i[0], i[1]), i[2], (0, 255, 0), 1)

        cv.imshow('block', block_to_draw)
        key = cv.waitKey(30)
        if key == 27:
            break

def testinng_circles_2(blocks):
    window_trackbars_name = 'trackbars'
    cv.namedWindow(window_trackbars_name)
    cv.createTrackbar('Threshold_high', window_trackbars_name, circle_param['high_t'], 255, empty_callback)
    cv.createTrackbar('Threshold_low', window_trackbars_name, circle_param['low_t'], 255, empty_callback)
    cv.createTrackbar('maxR', window_trackbars_name, circle_param['max_r'], 400, empty_callback)
    cv.createTrackbar('minR', window_trackbars_name, circle_param['min_r'], 250, empty_callback)
    cv.createTrackbar('minDist', window_trackbars_name, circle_param['min_d'], 250, empty_callback)



    while True:
        Threshold_high = cv.getTrackbarPos('Threshold_high', window_trackbars_name)
        Threshold_low = cv.getTrackbarPos('Threshold_low', window_trackbars_name)
        maxR = cv.getTrackbarPos('maxR', window_trackbars_name)
        minR = cv.getTrackbarPos('minR', window_trackbars_name)
        minDist = cv.getTrackbarPos('minDist', window_trackbars_name)
        for j,block in enumerate(blocks):
            block_to_draw = cv.cvtColor(block, cv.COLOR_HSV2BGR)
            block_to_draw = cv.cvtColor(block_to_draw, cv.COLOR_BGR2GRAY)
            circles = cv.HoughCircles(block_to_draw, cv.HOUGH_GRADIENT, 1, minDist, param1=Threshold_high,
                                  param2=Threshold_low, minRadius=minR, maxRadius=maxR)


            if circles is not None:
                circles = np.uint16(np.around(circles))
                for i in circles[0, :]:
                    # draw the outer circle
                    cv.circle(block_to_draw, (i[0], i[1]), i[2], (0, 255, 0), 1)

            block_to_draw = cv.resize(block_to_draw, None, fx=0.7, fy=0.7)
            cv.imshow('block'+str(j), block_to_draw)
        key = cv.waitKey(100)
        if key == 27:
            break
