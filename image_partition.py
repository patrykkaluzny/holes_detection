import cv2 as cv
import numpy as np


def detect_block(img):
    contours, hierarchy = cv.findContours(img, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    filtered_contures = []
    # areas=[]
    for contour in contours:
        area = cv.contourArea(contour)

        if area > 15000:
            # areas.append(area)
            filtered_contures.append(contour)
    # print(min(areas  ))
    return filtered_contures


def noise_remove_img(img):
    kernel_5 = np.ones((5, 5), np.uint8)
    kernel_3 = np.ones((3, 3), np.uint8)
    dilate = cv.dilate(img, kernel_3, iterations=3)

    opening = cv.morphologyEx(dilate,cv.MORPH_OPEN,kernel_3, iterations=2)
    # cv.imshow('dilate', dilate)

    erode = cv.erode(opening, kernel_3, iterations=16)
    closing = cv.morphologyEx(erode, cv.MORPH_CLOSE,kernel_3, iterations=0)
    # cv.imshow('erode', erode)
    # plt.imshow(erode, 'grey')
    # plt.show()
    return closing


def get_objects_from_img(img, contours):
    blocks = []
    resize = 1.2
    for contour in contours[1:]:  # skip first one because its image frame
        rect = cv.minAreaRect(contour)
        box = cv.boxPoints(rect)
        box = np.int0(box)
        w = rect[1][0]
        h = rect[1][1]
        xs = [i[0] for i in box]
        ys = [i[1] for i in box]
        x1 = min(xs)
        x2 = max(xs)
        y1 = min(ys)
        y2 = max(ys)

        rotated = False
        angle = rect[2]

        if angle < -45:
            angle += 90
            rotated = True

        center = (int((x1 + x2) / 2), int((y1 + y2) / 2))
        size = (int(resize * (x2 - x1)), int(resize * (y2 - y1)))

        M = cv.getRotationMatrix2D((size[0] / 2, size[1] / 2), angle, 1.0)

        cropped = cv.getRectSubPix(img, size, center)
        cropped = cv.warpAffine(cropped, M, size)

        cropped_w = w if not rotated else h
        cropped_h = h if not rotated else w

        cropped_rotated = cv.getRectSubPix(cropped, (int(cropped_w * resize), int(cropped_h * resize)),
                                           (size[0] / 2, size[1] / 2))
        blocks.append(cropped_rotated)

    return blocks


def enlarge(img, enlarge_size):
    if len(img.shape) == 2:
        row, col = img.shape[0:2]
        new_shape = [enlarge_size*2+row, enlarge_size*2+col]
        enlarge_img = np.full(new_shape, 255, dtype=np.uint8)
        enlarge_img[enlarge_size:enlarge_size+row, enlarge_size:enlarge_size+col] = img
        return enlarge_img
    else:
        row, col = img.shape[0:2]
        new_shape = [200+row, 200+col, 3]
        enlarge_img = np.zeros(new_shape,dtype=np.uint8)
        enlarge_img[100:100+row, 100:100+col, :3] = img
        return enlarge_img

