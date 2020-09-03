import cv2 as cv
import numpy as np


def empty_callback(value):
    pass



img = cv.imread('imgs/img_002.jpg',1)
window_result_name = 'hsv_img'
window_picker_name = 'trackbars'
window_img_name = 'img'
cv.namedWindow(window_result_name)
cv.namedWindow(window_picker_name)
cv.namedWindow(window_img_name)

cv.createTrackbar('hue_min', window_picker_name, 0, 360//2, empty_callback)
cv.createTrackbar('hue_max', window_picker_name, 360//2, 360//2, empty_callback)
cv.createTrackbar('sat_min', window_picker_name, 0, 255, empty_callback)
cv.createTrackbar('sat_max', window_picker_name, 100, 255, empty_callback)
cv.createTrackbar('val_min', window_picker_name, 0, 255, empty_callback)
cv.createTrackbar('val_max', window_picker_name, 100, 255, empty_callback)


img_HSV = cv.cvtColor(img.copy(), cv.COLOR_BGR2HSV)
while True:

    hue_min = cv.getTrackbarPos('hue_min', window_picker_name)
    hue_max = cv.getTrackbarPos('hue_max', window_picker_name)
    sat_min = cv.getTrackbarPos('sat_min', window_picker_name)
    sat_max = cv.getTrackbarPos('sat_max', window_picker_name)
    val_min = cv.getTrackbarPos('val_min', window_picker_name)
    val_max = cv.getTrackbarPos('val_max', window_picker_name)
    img_threshold = cv.inRange(img_HSV, (hue_min, sat_min, val_min), (hue_max, sat_max, val_max))

    img_threshold = cv.resize(img_threshold, None, fx=0.2, fy=0.2)
    cv.imshow(window_result_name, img_threshold)
    cv.imshow(window_img_name, cv.resize(img.copy(), None, fx=0.2, fy=0.2))
    key = cv.waitKey(30)
    if key == ord('q') or key == 27:
        break
