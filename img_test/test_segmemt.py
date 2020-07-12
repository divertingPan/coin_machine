# -*- coding: utf-8 -*-
# reference: https://zhuanlan.zhihu.com/p/38739563
import cv2
import numpy as np
import matplotlib.pyplot as plt


# img = cv2.imread('IMG_20200521_190255.jpg')
# img = cv2.imread('IMG_20200521_190301.jpg')
# img = cv2.imread('IMG_20200521_190338.jpg')
img = cv2.imread('IMG_20200521_190424.jpg')

img = cv2.resize(img, (768,1024), interpolation = cv2.INTER_AREA)
gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
gray = cv2.GaussianBlur(gray, (3,3), 0)
thresh = cv2.Canny(gray, 50, 150)

# only 2 return values after opencv3.2
_, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

def draw_min_rect_circle(img, cnts):  # conts = contours
    img = np.copy(img)

    max_area = 0
    for cnt in cnts:
        x, y, w, h = cv2.boundingRect(cnt)
        # cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)  # blue
        if w*h > max_area:
            max_area = w*h
            rec_x = x
            rec_y = y
            rec_w = w
            rec_h = h
        
        # min_rect = cv2.minAreaRect(cnt)  # min_area_rectangle
        # min_rect = np.int0(cv2.boxPoints(min_rect))
        # cv2.drawContours(img, [min_rect], 0, (0, 255, 0), 2)  # green

        # (x, y), radius = cv2.minEnclosingCircle(cnt)
        # center, radius = (int(x), int(y)), int(radius)  # for the minimum enclosing circle
        # img = cv2.circle(img, center, radius, (0, 0, 255), 2)  # red
    img = img[rec_y-1:rec_y+rec_h+1, rec_x-1:rec_x+rec_w+1]
    return img

img = draw_min_rect_circle(img, contours)

# cv2.imwrite('edge.png', thresh)
# cv2.imwrite('boundary.png', img)
cv2.imwrite('4.png', img)
cv2.imshow("img", img)
if cv2.waitKey(0) == 27:
    cv2.destroyAllWindows()

# reference: https://github.com/abidrahmank/OpenCV2-Python/blob/master/Official_Tutorial_Python_Codes/3_imgproc/canny.py

# def CannyThreshold(lowThreshold):
#     detected_edges = cv2.GaussianBlur(gray, (3,3), 0)
#     detected_edges = cv2.Canny(detected_edges, lowThreshold, lowThreshold*ratio, apertureSize=kernel_size)
#     dst = cv2.bitwise_and(img, img, mask=detected_edges)  # just add some colours to edges from original image.
#     cv2.imshow('canny demo', dst)
 
# lowThreshold = 0
# max_lowThreshold = 100
# ratio = 3
# kernel_size = 3
 
# img = cv2.imread('IMG_20200521_190424.jpg')
# img = cv2.resize(img, (480,640), interpolation = cv2.INTER_AREA)
# gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
 
# cv2.namedWindow('canny demo')
 
# cv2.createTrackbar('Min threshold', 'canny demo', lowThreshold, max_lowThreshold, CannyThreshold)
 
# CannyThreshold(0)  # initialization
# if cv2.waitKey(0) == 27:
#     cv2.destroyAllWindows()
