# -*- coding: utf-8 -*-
import numpy as np
import os
import cv2
import matplotlib.pyplot as plt
import pandas as pd
from skimage.feature import local_binary_pattern


def get_lbp_hist(img):
    radius = 3
    n_points = 8 * radius
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.resize(img, (200, 200))
    lbp = local_binary_pattern(img, n_points, radius, 'uniform')
    lbp2 = lbp.astype(np.uint8)
    max_bins = int(lbp2.max() + 1)
    hist, _ = np.histogram(lbp2, bins=max_bins, range=(0, max_bins))
    return hist


# reference: https://www.jianshu.com/p/3eaa970bd45c
def cosine_distance(matrix1, matrix2):
    matrix1_matrix2 = np.dot(matrix1, matrix2.transpose())
    matrix1_norm = np.sqrt(np.multiply(matrix1, matrix1).sum(axis=1))
    matrix1_norm = matrix1_norm[:, np.newaxis]
    matrix2_norm = np.sqrt(np.multiply(matrix2, matrix2).sum(axis=1))
    matrix2_norm = matrix2_norm[:, np.newaxis]
    cosine_distance = np.divide(matrix1_matrix2, np.dot(matrix1_norm, matrix2_norm.transpose()))
    return cosine_distance


data = {'test_file': ['test_file'], 'similar_coin': ['similar_coin'], 'score': ['score']}
dataframe = pd.DataFrame(data)
dataframe.to_csv(r'./coin_recognition_list.csv', header=False, index=False, encoding='utf-8_sig')

std_vector = []
for maindir, subdir, standard_list in os.walk('./standard_img'):
    for i, standard_file in enumerate(standard_list):
        standard_img = cv2.imread('./standard_img/%s' % standard_file)
        std_vector.append(get_lbp_hist(standard_img))
        print('%d/%d standard_img vector predicted' % (i + 1, len(standard_list)))

test_vector = []
for maindir, subdir, test_list in os.walk('./testing_img_seg'):
    for i, test_file in enumerate(test_list):
        test_img = cv2.imread('./testing_img_seg/%s' % test_file)
        test_vector.append(get_lbp_hist(test_img))
        print('%d/%d test_img vector predicted' % (i + 1, len(test_list)))

test_coin_list = []
similar_coin_list = []
score = []

test_vector = np.squeeze(np.array(test_vector))
std_vector = np.squeeze(np.array(std_vector))
cosine_dis = cosine_distance(test_vector, std_vector)

for i in range(cosine_dis.shape[0]):
    test_score = cosine_dis[i]
    j = np.argmax(test_score)
    data = {'test_file': [test_list[i]], 'similar_coin': [standard_list[j]], 'score': [np.max(test_score, axis=0)]}
    dataframe = pd.DataFrame(data)
    dataframe.to_csv(r'./coin_recognition_list.csv', mode='a', header=False, index=False, encoding='utf-8_sig')
    test_coin_list.append(test_list[i])
    similar_coin_list.append(standard_list[j])
    score.append(np.max(test_score, axis=0))


df = pd.read_csv('./coins.csv')
all_test_list = [x for x in df['test_file']]
all_similar_list = [x for x in df['similar_coin']]

score = 0
for i in test_coin_list:
    if all_similar_list[all_test_list.index(i)] == similar_coin_list[test_coin_list.index(i)]:
        score += 1
score = score / len(test_coin_list)
print(score)
