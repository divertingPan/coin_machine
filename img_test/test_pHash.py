# -*- coding: utf-8 -*-
import numpy as np
import cv2


# reference: https://www.cnblogs.com/dcb3688/p/4610660.html
def phash(img, size):
    #缩放32*32
    img = cv2.resize(img, (size, size), interpolation=cv2.INTER_CUBIC)

    # 将灰度图转为浮点型，再进行dct变换
    dct = cv2.dct(np.float32(img))
    #opencv实现的掩码操作
    dct_roi = dct[0:8, 0:8]

    hash = []
    avreage = np.mean(dct_roi)
    for i in range(dct_roi.shape[0]):
        for j in range(dct_roi.shape[1]):
            if dct_roi[i, j] > avreage:
                hash.append(1)
            else:
                hash.append(0)
    return hash


def hammingDist(s1, s2):
    assert len(s1) == len(s2)
    return sum([ch1 != ch2 for ch1, ch2 in zip(s1, s2)])


# pHash
test = cv2.imread('3.png', cv2.IMREAD_GRAYSCALE)
std = cv2.imread('sri_lanka-5-cents-1991.jpg', cv2.IMREAD_GRAYSCALE)
test = cv2.equalizeHist(test)
std = cv2.equalizeHist(std)
size = 64
test_hash = phash(test, size)
std_hash = phash(std, size)
score = 1 - hammingDist(test_hash, std_hash)*1./(64*64/4)
print(score)