import cv2 as cv
from variables import circle_param
def detect_circle(block):
    circles = cv.HoughCircles(block, cv.HOUGH_GRADIENT, circle_param['dp'], circle_param['min_d'], param1=circle_param['high_t'],
                              param2=circle_param['low_t'], minRadius=circle_param['min_r'], maxRadius=circle_param['max_r'])
    if circles is not None:
        return circles.shape[1]
    return 0
