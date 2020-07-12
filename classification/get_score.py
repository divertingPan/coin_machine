# -*- coding: utf-8 -*-
import pandas as pd


df = pd.read_csv('./coins.csv')
all_test_list = [x for x in df['test_file']]
all_similar_list = [x for x in df['similar_coin']]

df = pd.read_csv('./coin_recognition_list.csv')
test_coin_list = [x for x in df['test_file']]
similar_coin_list = [x for x in df['similar_coin']]

score = 0
for i in test_coin_list:
    if all_similar_list[all_test_list.index(i)] == similar_coin_list[test_coin_list.index(i)]:
        score += 1
score = score / len(test_coin_list)
print(score)
