# -*- coding: utf-8 -*-

import cv2
import os
import matplotlib.pyplot as plt

# img = cv2.imread('1.png')
# img = cv2.imread('2.png')
# img = cv2.imread('3.png')
# img = cv2.imread('4.png')
# img = cv2.imread('china-1-jiao-1997.jpg')

# img = cv2.GaussianBlur(img, (3,3), 0)
# thresh = cv2.Canny(img, 50, 100)

# cv2.imwrite('4.png', img)
# cv2.imshow("img", thresh)
# cv2.waitKey()


for maindir, subdir, file_name_list in os.walk('./'):
    for filename in file_name_list:
        apath = os.path.join(maindir, filename)
        
        img = cv2.imread(apath)
        img = cv2.GaussianBlur(img, (3,3), 0)
        thresh = cv2.Canny(img, 50, 100)

        cv2.imwrite('./edges/%s_edge.png' %filename, thresh)
        
        print(apath + 'saved: %s_edge' %filename)

            