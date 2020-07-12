# -*- coding: utf-8 -*-
import torchvision.models as models
import torch
import numpy as np
import os
import cv2
import matplotlib.pyplot as plt
import pandas as pd
import torch.nn as nn
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-n", "--num_classes", default=200, type=int, help="amount of classes")
args = parser.parse_args()


def get_prediction(img, net):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (224, 224))
    img = np.transpose(img, (2, 0, 1))
    img = np.expand_dims(img, axis=0)
    img = torch.from_numpy(img).float()
    with torch.no_grad():
        outputs = net(img).data.numpy()
    return outputs


# reference: https://www.jianshu.com/p/3eaa970bd45c
def cosine_distance(matrix1, matrix2):
    matrix1_matrix2 = np.dot(matrix1, matrix2.transpose())
    matrix1_norm = np.sqrt(np.multiply(matrix1, matrix1).sum(axis=1))
    matrix1_norm = matrix1_norm[:, np.newaxis]
    matrix2_norm = np.sqrt(np.multiply(matrix2, matrix2).sum(axis=1))
    matrix2_norm = matrix2_norm[:, np.newaxis]
    cosine_distance = np.divide(matrix1_matrix2, np.dot(matrix1_norm, matrix2_norm.transpose()))
    return cosine_distance


def Euclidean_distance(A, B):
    BT = B.transpose()
    vecProd = np.dot(A, BT)
    SqA = A ** 2
    sumSqA = np.matrix(np.sum(SqA, axis=1))
    sumSqAEx = np.tile(sumSqA.transpose(), (1, vecProd.shape[1]))

    SqB = B ** 2
    sumSqB = np.sum(SqB, axis=1)
    sumSqBEx = np.tile(sumSqB, (vecProd.shape[0], 1))
    SqED = sumSqBEx + sumSqAEx - 2 * vecProd
    SqED[SqED < 0] = 0.0
    ED = np.sqrt(SqED)
    return ED


data = {'test_file': ['test_file'], 'similar_coin': ['similar_coin'], 'score': ['score']}
dataframe = pd.DataFrame(data)
dataframe.to_csv(r'./coin_recognition_list.csv', header=False, index=False, encoding='utf-8_sig')

net = models.resnet50(pretrained=False)
# 全连接层的输入通道in_channels个数
num_fc_in = net.fc.in_features
# 改变全连接层
net.fc = nn.Linear(num_fc_in, args.num_classes)
net.load_state_dict(torch.load('./net.pth'))
net.eval()

std_vector = []
for maindir, subdir, standard_list in os.walk('./standard_img'):
    for i, standard_file in enumerate(standard_list):
        standard_img = cv2.imread('./standard_img/%s' % standard_file)
        std_vector.append(get_prediction(standard_img, net))
        print('%d/%d standard_img vector predicted' % (i + 1, len(standard_list)))

test_vector = []
for maindir, subdir, test_list in os.walk('./testing_img_seg'):
    for i, test_file in enumerate(test_list):
        test_img = cv2.imread('./testing_img_seg/%s' % test_file)
        test_vector.append(get_prediction(test_img, net))
        print('%d/%d test_img vector predicted' % (i + 1, len(test_list)))

test_coin_list = []
similar_coin_list = []
score = []

test_vector = np.squeeze(np.array(test_vector))
std_vector = np.squeeze(np.array(std_vector))
# cosine_dis = cosine_distance(test_vector, std_vector)
Euclidean_dis = Euclidean_distance(test_vector, std_vector)

for i in range(Euclidean_dis.shape[0]):
    test_score = Euclidean_dis[i]
    j = np.argmin(test_score)
    data = {'test_file': [test_list[i]], 'similar_coin': [standard_list[j]], 'score': [np.min(test_score, axis=1)]}
    dataframe = pd.DataFrame(data)
    dataframe.to_csv(r'./coin_recognition_list.csv', mode='a', header=False, index=False, encoding='utf-8_sig')
    test_coin_list.append(test_list[i])
    similar_coin_list.append(standard_list[j])
    score.append(np.min(test_score, axis=1))

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
