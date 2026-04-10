import jieba
from math import log

Total_neg = 0
Total_pos = 0
Total_N = 0
pos = {}
neg = {}
stopwords = []

# 建立停用词表
with open('cn_stopwords.txt', encoding='utf8') as f0:
    for stopword in f0:
        stopwords.append(stopword.strip())

#  抽取特征
for i in range(0, 2670):
    try:
        with open(f'.\htl_del_4000\\neg\\neg.{i}.txt', encoding='GBK', errors='ignore') as f1:
            for sentence_to_cut in f1:
                sentence = jieba.lcut(sentence_to_cut.strip())
                sentence = set(sentence)
                for word in sentence:
                    if word in stopwords:
                        continue
                    if word not in neg:
                        neg[word] = 1
                    else:
                        neg[word] += 1
                    if word not in pos:
                        pos[word] = 0.000001
            Total_N += 1
            Total_neg += 1
    except FileNotFoundError:
        continue

for i in range(4, 2670):
    try:
        with open(f'.\htl_del_4000\\pos\\pos.{i}.txt', encoding='GBK', errors='ignore') as f2:
            for sentence_to_cut in f2:
                sentence = jieba.lcut(sentence_to_cut.strip())
                for word in sentence:
                    if word in stopwords:
                        continue
                    if word not in pos:
                        pos[word] = 1
                    else:
                        pos[word] += 1
                    if word not in neg:
                        neg[word] = 0.000001
            Total_N += 1
            Total_pos += 1
    except FileNotFoundError:
        continue

# 初始化MI
MI_pos = {}
MI_neg = {}
for i in pos:
    if i not in MI_pos:
        MI_pos[i] = 0
    if i not in MI_neg:
        MI_neg[i] = 0

for i in neg:
    if i not in MI_neg:
        MI_neg[i] = 0
    if i not in MI_pos:
        MI_pos[i] = 0

for word, value in MI_pos.items():
    MI_pos[word] = log((pos[word] * Total_N) / (Total_pos * (pos[word] + neg[word])), 10)
for word, value in MI_neg.items():
    MI_neg[word] = log((neg[word] * Total_N) / (Total_neg * (pos[word] + neg[word])), 10)

MI = {}
for word, value in MI_pos.items():
    MI[word] = 0
for word, value in MI_pos.items():
    MI[word] = (MI_pos[word] + MI_neg[word]) / 2

MI = sorted(MI.items(), key=lambda x: x[1], reverse=True)
with open('互信息值.txt', 'w', encoding='utf8') as F:
    count = 0
    for word, value in MI:
        if count == 1000:
            break
        F.write(f"{word}:{value}\n")
        count += 1
