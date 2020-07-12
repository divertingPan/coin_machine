# -*- coding: utf-8 -*-


from skimage.feature import local_binary_pattern
import numpy as np
import matplotlib.pyplot as plt
import cv2

# settings for LBP
radius = 1  # LBP算法中范围半径的取值
n_points = 8 * radius # 领域像素点数

# 读取图像
# img = cv2.imread('coin.png')
img = cv2.imread('mozambique-10000-meticais-2003.jpg')
img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
img = cv2.resize(img, (128,128), interpolation = cv2.INTER_AREA)

# LBP
# lbp = local_binary_pattern(img, n_points, radius)

sift = cv2.xfeatures2d.SIFT_create()
kp = sift.detect(img, None)
ret = cv2.drawKeypoints(img, kp, img)

cv2.imshow("img", img)
cv2.waitKey()

# plt.imshow(lbp, 'gray')
# plt.show()

# hist, bins = np.histogram(lbp.ravel(), 256, [0,255])
# plt.plot(hist)
# plt.show()