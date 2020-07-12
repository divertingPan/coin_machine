# -*- coding: utf-8 -*-
import numpy as np
import os
import cv2
import matplotlib.pyplot as plt
import pandas as pd
from skimage.feature import local_binary_pattern


def get_edges(img):
    img = cv2.resize(img, (300, 300), interpolation=cv2.INTER_AREA)
    img = cv2.GaussianBlur(img, (5, 5), 0)
    thresh = cv2.Canny(img, 50, 100)
    return thresh


def recognition(test, std):
    # pixel detection
    test = get_edges(test)
    std = get_edges(std)
    test = test / 255
    std = std / 255
    score = (np.sum(test * std) * 2) / (np.sum(test) + np.sum(std))
    # score = np.sum(test * std) / np.sum(test)

    return score


data = {'test_file':['test_file'], 'similar_coin':['similar_coin'], 'score':['score']}
dataframe = pd.DataFrame(data)
dataframe.to_csv(r'./coin_recognition_list.csv', header=False, index=False, encoding='utf-8_sig')

test_coin_list = []
similar_coin_list = []
score = []

for maindir, subdir, test_list in os.walk('./testing_img_seg'):
    for i, test_file in enumerate(test_list):
        print('%d/%d testing: ' % (i+1, len(test_list)), test_file)
        test_img = cv2.imread('./testing_img_seg/%s' % test_file)

        max_overlay = 0
        similar_coin = 'None'
        for maindir, subdir, standard_list in os.walk('./standard_img'):
            for standard_file in standard_list:
                standard_img = cv2.imread('./standard_img/%s' % standard_file)

                overlay = recognition(test_img, standard_img)
                
                if overlay > max_overlay:
                    max_overlay = overlay
                    similar_coin = standard_file

        test_coin_list.append(test_file)
        similar_coin_list.append(similar_coin)
        score.append(max_overlay)
        
        data = {'test_file':[test_file], 'similar_coin':[similar_coin], 'score': [max_overlay]}
        dataframe = pd.DataFrame(data)
        dataframe.to_csv(r'./coin_recognition_list.csv', mode='a', header=False, index=False, encoding='utf-8_sig')

# print(test_coin_list)
# print(similar_coin_list)
# print(score)


df = pd.read_csv('./coins.csv')
all_test_list = [x for x in df['test_file']]
all_similar_list = [x for x in df['similar_coin']]

score = 0
for i in test_coin_list:
    if all_similar_list[all_test_list.index(i)] == similar_coin_list[test_coin_list.index(i)]:
        score += 1
score = score / len(test_coin_list)
print(score)
    

# test_img = cv2.imread('./standard_img/hong_kong-1-dollar-1992 (1).jpg', cv2.IMREAD_GRAYSCALE)
# test_img = get_edges(test_img)
# cv2.imwrite('./hk.jpg', test_img)
# test_img = cv2.imread('./standard_img/spain-25-pesetas-1983 (1).jpg', cv2.IMREAD_GRAYSCALE)
# image = cv2.equalizeHist(test_img)
# plt.imshow(image, 'gray')

