# -*- coding: utf-8 -*-

import numpy as np
import cv2
import matplotlib.pyplot as plt


img1 = cv2.imread('./edges/1.png_edge.png', cv2.IMREAD_GRAYSCALE)
img2 = cv2.imread('./edges/china-5-jiao-2007.jpg_edge.png', cv2.IMREAD_GRAYSCALE)
img1 = cv2.resize(img1, (200,200), interpolation = cv2.INTER_AREA)
img2 = cv2.resize(img2, (200,200), interpolation = cv2.INTER_AREA)

img3 = cv2.imread('./edges/mozambique-10000-meticais-2003.jpg_edge.png', cv2.IMREAD_GRAYSCALE)
img3 = cv2.resize(img3, (200,200), interpolation = cv2.INTER_AREA)

# plt.imshow(img1, 'gray')
# plt.show()
# plt.imshow(img2, 'gray')
# plt.show()

img1 = img1 / 255
img2 = img2 / 255

img = img1 * img2
plt.imshow(img, 'gray')

overlay = (np.sum(img) * 2) / (np.sum(img1) + np.sum(img2))
print(overlay)