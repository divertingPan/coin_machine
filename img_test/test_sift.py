# -*- coding: utf-8 -*-
# reference: https://www.mscto.com/python/24277.html

import cv2
import matplotlib.pyplot as plt
import numpy as np


min_match_count = 10
img1 = cv2.imread('IMG_20150927_094426.jpg', cv2.IMREAD_GRAYSCALE)  # query image
img2 = cv2.imread('IMG_20150927_094430.jpg', cv2.IMREAD_GRAYSCALE)  # train image
 
# Initiate SIFT detector
sift = cv2.xfeatures2d.SURF_create()
# find the keypoints and descriptors with SIFT
kp1, des1 = sift.detectAndCompute(img1, None)
kp2, des2 = sift.detectAndCompute(img2, None)
 
flann_index_kdtree = 0
index_params = dict(algorithm=flann_index_kdtree, trees=5)
search_params = dict(checks=50)
flann = cv2.FlannBasedMatcher(index_params, search_params)
matches = flann.knnMatch(des1, des2, k=2)
 
# store all the good matches as per Lowe's ratio test
good = []
for m, n in matches:
    if m.distance < 0.7 * n.distance:
        good.append(m)
 
'''
设置只有存在10个以上匹配时，采取查找目标 min_match_count=10，否则显示特征点匹配不了
如果找到了足够的匹配，就提取两幅图像中匹配点的坐标，把它们传入到函数中做变换
'''
if len(good) > min_match_count:
    # 获取关键点的坐标
    src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
    dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
    # 第三个参数 Method used to computed a homography matrix.
    #  The following methods are possible: #0 - a regular method using all the points
    # CV_RANSAC - RANSAC-based robust method
    # CV_LMEDS - Least-Median robust method
    # 第四个参数取值范围在 1 到 10  绝一个点对的 值。原图像的点经 变换后点与目标图像上对应点的 差 #    差就 为是 outlier
    #  回值中 M 为变换矩
    M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
    matchesMask = mask.ravel().tolist()
    # 获取原图像的高和宽
    h, w = img1.shape
    # 使用得到的变换矩阵对原图想的四个变换获得在目标图像上的坐标
    pts = np.float32([[0, 0], [0, h -1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
    dst = cv2.perspectiveTransform(pts, M)
    # 将原图像转换为灰度图
    img2 = cv2.polylines(img2, [np.int32(dst)], True, 255, 3, cv2.LINE_AA)
else:
    print('Not enough matches are found - %d/%d' % (len(good), min_match_count))
    matchesMask = None
 
# 最后在绘制inliers，如果能成功找到目标图像的话或者匹配关键点失败
draw_params = dict(matchColor=(0, 255, 0),
                   singlePointColor=None,
                   matchesMask=matchesMask,
                   flags=2)
img3 = cv2.drawMatches(img1, kp1, img2, kp2, good, None, **draw_params)
plt.imshow(img3, cmap='gray')
plt.show()
