# -*- coding: utf-8 -*-
# reference: https://zhuanlan.zhihu.com/p/38739563
import cv2
import os
import numpy as np
import matplotlib.pyplot as plt


def draw_min_rect_circle(img, cnts):  # conts = contours
    img = np.copy(img)

    max_area = 0
    for cnt in cnts:
        x, y, w, h = cv2.boundingRect(cnt)
        # cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        if w*h > max_area and 0.8 < w/h < 1.25:
            max_area = w*h
            rec_x = x
            rec_y = y
            rec_w = w
            rec_h = h

    img = img[rec_y:rec_y+rec_h, rec_x:rec_x+rec_w]
    
    return img


for maindir, subdir, file_name_list in os.walk('./testing_img'):
    for filename in file_name_list:
        apath = os.path.join(maindir, filename)
        img = cv2.imread(apath)
        img = cv2.resize(img, (1536, 2048), interpolation=cv2.INTER_AREA)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (3, 3), 0)
        thresh = cv2.Canny(gray, 10, 100)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 25))
        closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

        # only 2 return values after opencv3.2
        _, contours, hierarchy = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        img = draw_min_rect_circle(img, contours)

        filename = os.path.splitext(filename)[0]
        cv2.imwrite('./testing_img_seg/%s.jpg' % filename, img)
        # images for testing observing
        cv2.imwrite('./testing_img_seg/%s_closed.jpg' % filename, closed)
        cv2.imwrite('./testing_img_seg/%s_gray.jpg' % filename, gray)
        cv2.imwrite('./testing_img_seg/%s_thresh.jpg' % filename, thresh)

        print('saved: testing_img_seg/%s' % filename)


"""
img = cv2.imread('./testing_img/IMG_20200526_153332.jpg')
filename = 'IMG_20200526_153332'
img = cv2.resize(img, (1536, 2048), interpolation=cv2.INTER_AREA)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (3, 3), 0)
thresh = cv2.Canny(gray, 10, 100)

plt.imshow(thresh, 'gray')
cv2.imwrite('./testing_img_seg/%s_thresh.jpg' % filename, thresh)

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9))

# dilation
for i in range(5):
    thresh = cv2.dilate(thresh, kernel)
    plt.imshow(thresh, 'gray')
    cv2.imwrite('./testing_img_seg/%s_dilation_%d.jpg' % (filename, i), thresh)

# erosion
for i in range(10):
    thresh = cv2.erode(thresh, kernel)
    plt.imshow(thresh, 'gray')
    cv2.imwrite('./testing_img_seg/%s_erosion_%d.jpg' % (filename, i), thresh)

# dilation
for i in range(5):
    thresh = cv2.dilate(thresh, kernel)
    plt.imshow(thresh, 'gray')
    cv2.imwrite('./testing_img_seg/%s_dilation_%d.jpg' % (filename, i+5), thresh)


# close and open
thresh = cv2.Canny(gray, 10, 100)
closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=5)
cv2.imwrite('./testing_img_seg/%s_closed.jpg' % filename, closed)
opened = cv2.morphologyEx(closed, cv2.MORPH_OPEN, kernel, iterations=5)
cv2.imwrite('./testing_img_seg/%s_opened.jpg' % filename, opened)

"""

"""
# reference: https://blog.csdn.net/liqiancao/article/details/55670749
for maindir, subdir, file_name_list in os.walk('./testing_img'):
    for filename in file_name_list:
        
        apath = os.path.join(maindir, filename)
        img = cv2.imread(apath)
        img = cv2.resize(img, (1536, 2048), interpolation=cv2.INTER_AREA)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        gradX = cv2.Sobel(gray, ddepth=cv2.CV_32F, dx=1, dy=0, ksize=-1)
        gradY = cv2.Sobel(gray, ddepth=cv2.CV_32F, dx=0, dy=1, ksize=-1)

        # subtract the y-gradient from the x-gradient
        gradient = cv2.subtract(gradX, gradY)
        gradient = cv2.convertScaleAbs(gradient)
        
        # blur and threshold the image
        blurred = cv2.blur(gradient, (9, 9))
        (_, thresh) = cv2.threshold(blurred, 90, 255, cv2.THRESH_BINARY)
        
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (50, 50))
        closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

        # only 2 return values after opencv3.2
        _, contours, hierarchy = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        img = draw_min_rect_circle(img, contours)

        # reference: https://blog.csdn.net/m0_38007695/article/details/82718107
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        gray = clahe.apply(gray)
        
        gray = cv2.GaussianBlur(gray, (3, 3), 0)
        thresh = cv2.Canny(gray, 50, 150)

        filename = os.path.splitext(filename)[0]
        cv2.imwrite('./testing_img_seg_check/%s.jpg' % filename, img)
        cv2.imwrite('./testing_img_seg_check/%s_closed.jpg' % filename, closed)
        cv2.imwrite('./testing_img_seg_check/%s_gray.jpg' % filename, gray)
        cv2.imwrite('./testing_img_seg_check/%s_thresh.jpg' % filename, thresh)

        print('saved: edges/%s' % filename)
        
"""