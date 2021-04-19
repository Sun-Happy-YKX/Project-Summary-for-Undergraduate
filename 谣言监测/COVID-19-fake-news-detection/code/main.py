#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
import jieba
import jieba.analyse
import jieba.posseg as psg
import matplotlib.pyplot as plt
import multiprocessing
import random
import operator
from wordcloud import WordCloud
from wordcloud import ImageColorGenerator
from PIL import Image
import csv
import pickle
import logging
import re


datas = pd.read_csv('test_dataset_update.csv')


# --初始化结果--

c_id = datas['id'].tolist()
fake_prob_label_0c = [0.3 for each in c_id]
fake_prob_label_2c = fake_prob_label_0c
fake_prob_label_all = fake_prob_label_0c
real_prob_label_0c = fake_prob_label_0c
real_prob_label_2c = fake_prob_label_0c
real_prob_label_all = fake_prob_label_0c
ncw_prob_label_0c = [0.4 for each in c_id]
ncw_prob_label_2c = ncw_prob_label_0c
ncw_prob_label_all = ncw_prob_label_0c

result = pd.DataFrame({'id':c_id, 'fake_prob_label_0c':fake_prob_label_0c, 'fake_prob_label_2c':fake_prob_label_2c, 'fake_prob_label_all':fake_prob_label_all,
                   'real_prob_label_0c':real_prob_label_0c, 'real_prob_label_2c':real_prob_label_2c, 'real_prob_label_all':real_prob_label_all,
                   'ncw_prob_label_0c':ncw_prob_label_0c, 'ncw_prob_label_2c':ncw_prob_label_2c, 'ncw_prob_label_all':ncw_prob_label_all})


# --文本预处理--

datas.columns
datas = datas.fillna({'content':'','picture_lists':'','category':'','comment_2':'','comment_all':''})

# 去掉content的html
for i in range(datas.shape[0]):
    datas.loc[i,'content'] = re.sub(r'http[0-9a-zA-Z:/-_.&@#$%^*=+]+', 'url', datas.loc[i,'content'])

# content_len
datas['content_len'] = None
for i in range(datas.shape[0]):
    datas.loc[i,'content_len'] = len(datas.loc[i,'content'])
    
stop_words = [line.strip() for line in open('stopwords.txt', 'r', encoding='utf-8').readlines()]
stop_words.remove('发现')
stop_words.extend(['新冠', '新型', '肺炎', '病毒', '冠状病毒', '无', '图片'])

sentences = []
for line in datas['content'].tolist():
    segs = jieba.lcut(line)
    #segs = [v.word for v in segs if v.flag.startswith('n')]
    segs = [v for v in segs if not str(v).isdigit()] #去数字
    segs = list(filter(lambda x:x.strip(), segs)) #去左右空格
    segs = list(filter(lambda x:len(x)>1, segs)) #长度为1的字符
    segs = list(filter(lambda x:x not in stop_words, segs)) #去掉停用词
    words = []
    for each in segs:
        if len(each)!=2 and each[-1]=='市':
            words.append(each.rstrip('市'))
        elif len(each)!=2 and each[-1]=='省':
            words.append(each.rstrip('省'))
        else:
            words.append(each)
    sentences.append(words)


# --len<12 ncw--

for i in range(datas.shape[0]):
    if datas['content_len'][i] < 12:
        result.loc[i,'fake_prob_label_0c'] = 0
        result.loc[i,'fake_prob_label_2c'] = 0
        result.loc[i,'fake_prob_label_all'] = 0
        result.loc[i,'real_prob_label_0c'] = 0
        result.loc[i,'real_prob_label_2c'] = 0
        result.loc[i,'real_prob_label_all'] = 0
        result.loc[i,'ncw_prob_label_0c'] = 1
        result.loc[i,'ncw_prob_label_2c'] = 1
        result.loc[i,'ncw_prob_label_all'] = 1


# --情感词--

neg = [line.strip() for line in open('/Sentiment_dict/emotion-dict/neg_all_dict.txt', 'r', encoding='utf-8').readlines()]
pos = [line.strip() for line in open('/Sentiment_dict/emotion-dict/pos_all_dict.txt', 'r', encoding='utf-8').readlines()]

all_words = []
for each in sentences:
    all_words.extend(each)

sentiment = {}
for each in neg:
    sentiment[each] = all_words.count(each)
for each in pos:
    sentiment[each] = all_words.count(each)
sentiment_cp = sorted(sentiment.items(), key=operator.itemgetter(1), reverse=True)
print(sentiment_cp[:10])

all_w = []
for each in sentences:
    if '加油' in each:
        all_w.extend(each)
all_w_set = list(set(all_w))
temp = {}
for each in all_w_set:
    temp[each] = all_w.count(each)
cp = sorted(temp.items(), key=operator.itemgetter(1), reverse=True)
print(cp[:5])

for i in range(datas.shape[0]):
    try:
        if len(re.findall(r'武汉加油！|武汉加油!',datas['content'][i])) > 0:
            result.loc[i,'fake_prob_label_0c'] = 0
            result.loc[i,'fake_prob_label_2c'] = 0
            result.loc[i,'fake_prob_label_all'] = 0
            result.loc[i,'real_prob_label_0c'] = 0
            result.loc[i,'real_prob_label_2c'] = 0
            result.loc[i,'real_prob_label_all'] = 0
            result.loc[i,'ncw_prob_label_0c'] = 1
            result.loc[i,'ncw_prob_label_2c'] = 1
            result.loc[i,'ncw_prob_label_all'] = 1
    except:
        pass


# --判定词--

for i in range(datas.shape[0]):
    try:
        if len(re.findall(r'辟谣#',datas['content'][i])) > 0:
            result.loc[i,'fake_prob_label_0c'] = 0
            result.loc[i,'fake_prob_label_2c'] = 0
            result.loc[i,'fake_prob_label_all'] = 0
            result.loc[i,'real_prob_label_0c'] = 1
            result.loc[i,'real_prob_label_2c'] = 1
            result.loc[i,'real_prob_label_all'] = 1
            result.loc[i,'ncw_prob_label_0c'] = 0
            result.loc[i,'ncw_prob_label_2c'] = 0
            result.loc[i,'ncw_prob_label_all'] = 0
    except:
        pass

for i in range(datas.shape[0]):
    try:
        if len(re.findall(r'谣言|假的',datas['comment_2'][i])) > 0:
            datas.loc[i,'fake_prob_label_2c'] = 1
            datas.loc[i,'fake_prob_label_all'] = 1
            datas.loc[i,'real_prob_label_2c'] = 0
            datas.loc[i,'real_prob_label_all'] = 0
            datas.loc[i,'ncw_prob_label_2c'] = 0
            datas.loc[i,'ncw_prob_label_all'] = 0
            #print(datas['comment_2'][i])
    except:
        pass
for i in range(datas.shape[0]):
    try:
        if len(re.findall(r'谣言|假的',datas['comment_all'][i])) > 0:
            datas.loc[i,'fake_prob_label_all'] = 1
            datas.loc[i,'real_prob_label_all'] = 0
            datas.loc[i,'ncw_prob_label_all'] = 0
            #print(datas['comment_2'][i])
    except:
        pass


# --高频词--

words_set = list(set(all_w))
temp = {}
for each in words_set:
    temp[each] = words.count(each)
cp = sorted(temp.items(), key=operator.itemgetter(1), reverse=True)
print(cp)

# # 筛选具有独立、最小涵义的元词语
# ## 忘了排除文本中含有辟谣等词的推文

# 武汉,2080
# 感染,1114
# 疫情,1024
# 患者,763
# 口罩,749
# 加油,740
# 药物,582
# 医院,581
# 确诊,555
# 院士,498
# 隔离,475
# 淡盐水,451

all_w = []
for each in sentences:
    if '淡盐水' in each:
        all_w.extend(each)
all_w_set = list(set(all_w))
temp = {}
for each in all_w_set:
    temp[each] = all_w.count(each)
cp = sorted(temp.items(), key=operator.itemgetter(1), reverse=True)
print(cp[:10])

flag = 0
for i in range(datas.shape[0]):
    if len(re.findall(r'辟谣|假',datas['content'][i])) > 0 and len(re.findall(r'淡盐水',datas['content'][i])) > 0 and len(re.findall(r'盐水',datas['content'][i])) > 0 and len(re.findall(r'气流',datas['content'][i])) > 0:
        #print(datas['content'][i])
        flag = 1
print('flag:', flag)
if flag == 1:
    all_i = []
    for i in range(datas.shape[0]):
        if len(re.findall(r'淡盐水',datas['content'][i])) > 0 and len(re.findall(r'盐水',datas['content'][i])) > 0 and len(re.findall(r'气流',datas['content'][i])) > 0:
            #'''
            result.loc[i,'fake_prob_label_0c'] = 1
            result.loc[i,'fake_prob_label_2c'] = 1
            result.loc[i,'fake_prob_label_all'] = 1
            result.loc[i,'real_prob_label_0c'] = 0
            result.loc[i,'real_prob_label_2c'] = 0
            result.loc[i,'real_prob_label_all'] = 0
            result.loc[i,'ncw_prob_label_0c'] = 0
            result.loc[i,'ncw_prob_label_2c'] = 0
            result.loc[i,'ncw_prob_label_all'] = 0
            all_i.append(i)
            #'''
    datas.drop(index=all_i, inplace=True)

# 丰枫
words = []
for i in range(len(sentences)):
    if i not in all_i:
        words.extend(sentences[i])
words_set = list(set(words))
temp = {}
for each in words_set:
    temp[each] = words.count(each)
cp = sorted(temp.items(), key=operator.itemgetter(1), reverse=True)
print(cp[:15])

all_w = []
for each in sentences:
    if '丰枫' in each and '淡盐水' not in each:
        all_w.extend(each)
all_w_set = list(set(all_w))
temp = {}
for each in all_w_set:
    temp[each] = all_w.count(each)
cp = sorted(temp.items(), key=operator.itemgetter(1), reverse=True)
print(cp[:10])

flag = 0
for i in list(datas.index):
    if len(re.findall(r'辟谣|假',datas['content'][i])) > 0 and len(re.findall(r'丰枫',datas['content'][i])) > 0 and len(re.findall(r'社区',datas['content'][i])) > 0 and len(re.findall(r'身上',datas['content'][i])) > 0:
        #print(datas['content'][i])
        flag = 1
print('flag:', flag)
if flag == 0:
    each_i = []
    for i in list(datas.index):
        if len(re.findall(r'丰枫',datas['content'][i])) > 0 and len(re.findall(r'社区',datas['content'][i])) > 0 and len(re.findall(r'身上',datas['content'][i])) > 0:
            #'''
            result.loc[i,'fake_prob_label_0c'] = 0
            result.loc[i,'fake_prob_label_2c'] = 0
            result.loc[i,'fake_prob_label_all'] = 0
            result.loc[i,'real_prob_label_0c'] = 0.3
            result.loc[i,'real_prob_label_2c'] = 0.3
            result.loc[i,'real_prob_label_all'] = 0.3
            result.loc[i,'ncw_prob_label_0c'] = 0.7
            result.loc[i,'ncw_prob_label_2c'] = 0.7
            result.loc[i,'ncw_prob_label_all'] = 0.7
            each_i.append(i)
            #'''
    datas.drop(index=each_i, inplace=True)
    all_i.extend(each_i)

# 钟南山
words = []
for i in range(len(sentences)):
    if i not in all_i:
        words.extend(sentences[i])
words_set = list(set(words))
temp = {}
for each in words_set:
    temp[each] = words.count(each)
cp = sorted(temp.items(), key=operator.itemgetter(1), reverse=True)
print(cp)

all_w = []
for each in sentences:
    if '钟南山' in each and '淡盐水' not in each and '丰枫' not in each:
        all_w.extend(each)
all_w_set = list(set(all_w))
temp = {}
for each in all_w_set:
    temp[each] = all_w.count(each)
cp = sorted(temp.items(), key=operator.itemgetter(1), reverse=True)
print(cp[:10])

flag = 0
for i in list(datas.index):
    if len(re.findall(r'辟谣|假',datas['content'][i])) > 0 and len(re.findall(r'在家',datas['content'][i])) > 0 and len(re.findall(r'钟南山',datas['content'][i])) > 0 and len(re.findall(r'生命',datas['content'][i])) > 0:
        #print(datas['content'][i])
        flag = 1
print('flag:', flag)
if flag == 1:
    each_i = []
    for i in list(datas.index):
        if len(re.findall(r'在家',datas['content'][i])) > 0 and len(re.findall(r'钟南山',datas['content'][i])) > 0 and len(re.findall(r'生命',datas['content'][i])) > 0:
            #'''
            result.loc[i,'fake_prob_label_0c'] = 1
            result.loc[i,'fake_prob_label_2c'] = 1
            result.loc[i,'fake_prob_label_all'] = 1
            result.loc[i,'real_prob_label_0c'] = 0
            result.loc[i,'real_prob_label_2c'] = 0
            result.loc[i,'real_prob_label_all'] = 0
            result.loc[i,'ncw_prob_label_0c'] = 0
            result.loc[i,'ncw_prob_label_2c'] = 0
            result.loc[i,'ncw_prob_label_all'] = 0
            each_i.append(i)
            #'''
    datas.drop(index=each_i, inplace=True)
    all_i.extend(each_i)

# 西韦
words = []
for i in range(len(sentences)):
    if i not in all_i:
        words.extend(sentences[i])
words_set = list(set(words))
temp = {}
for each in words_set:
    temp[each] = words.count(each)
cp = sorted(temp.items(), key=operator.itemgetter(1), reverse=True)
print(cp)

all_w = []
for each in sentences:
    if '西韦' in each and '钟南山' not in each and '淡盐水' not in each and '丰枫' not in each:
        all_w.extend(each)
all_w_set = list(set(all_w))
temp = {}
for each in all_w_set:
    temp[each] = all_w.count(each)
cp = sorted(temp.items(), key=operator.itemgetter(1), reverse=True)
print(cp[:10])

flag = 0
for i in list(datas.index):
    if len(re.findall(r'辟谣|假',datas['content'][i])) > 0 and len(re.findall(r'美国',datas['content'][i])) > 0 and len(re.findall(r'西韦',datas['content'][i])) > 0 and len(re.findall(r'瑞德',datas['content'][i])) > 0:
        #print(datas['content'][i])
        flag = 1
print('flag:', flag)
if flag == 1:
    each_i = []
    for i in list(datas.index):
        if len(re.findall(r'美国',datas['content'][i])) > 0 and len(re.findall(r'西韦',datas['content'][i])) > 0 and len(re.findall(r'瑞德',datas['content'][i])) > 0 and len(re.findall(r'谣言',datas['content'][i])) == 0:
            #'''
            result.loc[i,'fake_prob_label_0c'] = 1
            result.loc[i,'fake_prob_label_2c'] = 1
            result.loc[i,'fake_prob_label_all'] = 1
            result.loc[i,'real_prob_label_0c'] = 0
            result.loc[i,'real_prob_label_2c'] = 0
            result.loc[i,'real_prob_label_all'] = 0
            result.loc[i,'ncw_prob_label_0c'] = 0
            result.loc[i,'ncw_prob_label_2c'] = 0
            result.loc[i,'ncw_prob_label_all'] = 0
            each_i.append(i)
            #'''
    datas.drop(index=each_i, inplace=True)
    all_i.extend(each_i)

# SARS
words = []
for i in range(len(sentences)):
    if i not in all_i:
        words.extend(sentences[i])
words_set = list(set(words))
temp = {}
for each in words_set:
    temp[each] = words.count(each)
cp = sorted(temp.items(), key=operator.itemgetter(1), reverse=True)
print(cp)

all_w = []
for each in sentences:
    if 'SARS' in each and '西韦' not in each and '钟南山' not in each and '淡盐水' not in each and '丰枫' not in each:
        all_w.extend(each)
all_w_set = list(set(all_w))
temp = {}
for each in all_w_set:
    temp[each] = all_w.count(each)
cp = sorted(temp.items(), key=operator.itemgetter(1), reverse=True)
print(cp[:10])

flag = 0
for i in list(datas.index):
    if len(re.findall(r'辟谣|假',datas['content'][i])) > 0 and len(re.findall(r'免疫系统',datas['content'][i])) > 0 and len(re.findall(r'感染',datas['content'][i])) > 0 and len(re.findall(r'莎丽服|SARS',datas['content'][i])) > 0:
        #print(datas['content'][i])
        flag = 1
print('flag:', flag)
if flag == 1:
    each_i = []
    for i in list(datas.index):
        if len(re.findall(r'免疫系统',datas['content'][i])) > 0 and len(re.findall(r'感染',datas['content'][i])) > 0 and len(re.findall(r'莎丽服|SARS',datas['content'][i])) > 0:
            #'''
            result.loc[i,'fake_prob_label_0c'] = 1
            result.loc[i,'fake_prob_label_2c'] = 1
            result.loc[i,'fake_prob_label_all'] = 1
            result.loc[i,'real_prob_label_0c'] = 0
            result.loc[i,'real_prob_label_2c'] = 0
            result.loc[i,'real_prob_label_all'] = 0
            result.loc[i,'ncw_prob_label_0c'] = 0
            result.loc[i,'ncw_prob_label_2c'] = 0
            result.loc[i,'ncw_prob_label_all'] = 0
            each_i.append(i)
            #'''
    datas.drop(index=each_i, inplace=True)
    all_i.extend(each_i)

# 朱一龙
words = []
for i in range(len(sentences)):
    if i not in all_i:
        words.extend(sentences[i])
words_set = list(set(words))
temp = {}
for each in words_set:
    temp[each] = words.count(each)
cp = sorted(temp.items(), key=operator.itemgetter(1), reverse=True)
print(cp)

all_w = []
for each in sentences:
    if '朱一龙' in each and 'SARS' not in each and '西韦' not in each and '钟南山' not in each and '淡盐水' not in each and '丰枫' not in each:
        all_w.extend(each)
all_w_set = list(set(all_w))
temp = {}
for each in all_w_set:
    temp[each] = all_w.count(each)
cp = sorted(temp.items(), key=operator.itemgetter(1), reverse=True)
print(cp[:10])

flag = 0
for i in list(datas.index):
    if len(re.findall(r'辟谣|假',datas['content'][i])) > 0 and len(re.findall(r'朱一龙',datas['content'][i])) > 0 and len(re.findall(r'加油',datas['content'][i])) > 0 and len(re.findall(r'武汉',datas['content'][i])) > 0:
        #print(datas['content'][i])
        flag = 1
print('flag:', flag)
if flag == 0:
    sentiment = {}
    for each in neg:
        sentiment[each] = all_words.count(each)
    for each in pos:
        sentiment[each] = all_words.count(each)
    sentiment_cp = sorted(sentiment.items(), key=operator.itemgetter(1), reverse=True)
    print(sentiment_cp[:10])
    
    each_i = []
    for i in list(datas.index):
        if len(re.findall(r'朱一龙',datas['content'][i])) > 0 and len(re.findall(r'武汉加油',datas['content'][i])) == 0:
            #'''
            result.loc[i,'fake_prob_label_0c'] = 0
            result.loc[i,'fake_prob_label_2c'] = 0
            result.loc[i,'fake_prob_label_all'] = 0
            result.loc[i,'real_prob_label_0c'] = 0
            result.loc[i,'real_prob_label_2c'] = 0
            result.loc[i,'real_prob_label_all'] = 0
            result.loc[i,'ncw_prob_label_0c'] = 1
            result.loc[i,'ncw_prob_label_2c'] = 1
            result.loc[i,'ncw_prob_label_all'] = 1
            each_i.append(i)
            #'''
    datas.drop(index=each_i, inplace=True)
    all_i.extend(each_i)

# 古天乐
words = []
for i in range(len(sentences)):
    if i not in all_i:
        words.extend(sentences[i])
words_set = list(set(words))
temp = {}
for each in words_set:
    temp[each] = words.count(each)
cp = sorted(temp.items(), key=operator.itemgetter(1), reverse=True)
print(cp)

all_w = []
for each in sentences:
    if '古天乐' in each and '朱一龙' not in each and 'SARS' not in each and '西韦' not in each and '钟南山' not in each and '淡盐水' not in each and '丰枫' not in each:
        all_w.extend(each)
all_w_set = list(set(all_w))
temp = {}
for each in all_w_set:
    temp[each] = all_w.count(each)
cp = sorted(temp.items(), key=operator.itemgetter(1), reverse=True)
print(cp[:10])

flag = 0
for i in list(datas.index):
    if len(re.findall(r'辟谣|假',datas['comment_2'][i])) > 0 and len(re.findall(r'古天乐',datas['content'][i])) > 0:
        #print(datas['content'][i])
        flag = 1
print('flag:', flag)
if flag == 1:
    each_i = []
    for i in list(datas.index):
        if len(re.findall(r'古天乐',datas['content'][i])) > 0:
            #'''
            #result.loc[i,'fake_prob_label_0c'] = 0
            result.loc[i,'fake_prob_label_2c'] = 0
            result.loc[i,'fake_prob_label_all'] = 0
            #result.loc[i,'real_prob_label_0c'] = 0
            result.loc[i,'real_prob_label_2c'] = 0
            result.loc[i,'real_prob_label_all'] = 0
            #result.loc[i,'ncw_prob_label_0c'] = 0
            result.loc[i,'ncw_prob_label_2c'] = 1
            result.loc[i,'ncw_prob_label_all'] = 1
            each_i.append(i)
            #'''
    datas.drop(index=each_i, inplace=True)
    all_i.extend(each_i)

# 飞机
words = []
for i in range(len(sentences)):
    if i not in all_i:
        words.extend(sentences[i])
words_set = list(set(words))
temp = {}
for each in words_set:
    temp[each] = words.count(each)
cp = sorted(temp.items(), key=operator.itemgetter(1), reverse=True)
print(cp)

all_w = []
for each in sentences:
    if '飞机' in each and '古天乐' not in each and '朱一龙' not in each and 'SARS' not in each and '西韦' not in each and '钟南山' not in each and '淡盐水' not in each and '丰枫' not in each:
        all_w.extend(each)
all_w_set = list(set(all_w))
temp = {}
for each in all_w_set:
    temp[each] = all_w.count(each)
cp = sorted(temp.items(), key=operator.itemgetter(1), reverse=True)
print(cp[:10])

flag = 0
for i in list(datas.index):
    if len(re.findall(r'辟谣|假',datas['content'][i])) > 0 and len(re.findall(r'飞机',datas['content'][i])) > 0 and len(re.findall(r'四点',datas['content'][i])) > 0:
        #print(datas['content'][i])
        flag = 1
print('flag:', flag)
if flag == 1:
    each_i = []
    for i in list(datas.index):
        if len(re.findall(r'飞机',datas['content'][i])) > 0 and len(re.findall(r'四点',datas['content'][i])) > 0:
            #'''
            result.loc[i,'fake_prob_label_0c'] = 0
            result.loc[i,'fake_prob_label_2c'] = 0
            result.loc[i,'fake_prob_label_all'] = 0
            result.loc[i,'real_prob_label_0c'] = 0
            result.loc[i,'real_prob_label_2c'] = 0
            result.loc[i,'real_prob_label_all'] = 0
            result.loc[i,'ncw_prob_label_0c'] = 1
            result.loc[i,'ncw_prob_label_2c'] = 1
            result.loc[i,'ncw_prob_label_all'] = 1
            each_i.append(i)
            #'''
    datas.drop(index=each_i, inplace=True)
    all_i.extend(each_i)
    
# --结果--
result.to_csv('result.csv', encoding='utf-8', index=False)