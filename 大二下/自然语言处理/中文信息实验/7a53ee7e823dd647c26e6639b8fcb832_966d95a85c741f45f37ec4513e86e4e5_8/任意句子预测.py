from math import log

import numpy
import torch
from gensim.models import word2vec
import jieba
import pickle

model = word2vec.Word2Vec.load("Skip-Gram.model")
word_fre = {}

with open('w2v_LogisticRegression_model.pickle', 'rb')as fin:
    Log_model = pickle.load(fin)

sentence_input = input("请输入要预测的句子：")
sentence_input = jieba.lcut(sentence_input.strip())

for i in range(0, 2670):
    try:
        with open(f'.\htl_del_4000\\neg\\neg.{i}.txt', encoding='GBK', errors='ignore') as f1:
            for sentence in f1:
                sentence = set(jieba.lcut(sentence.strip()))
                for word in sentence:
                    if word not in word_fre:
                        word_fre[word] = 1
                    else:
                        word_fre[word] += 1

    except FileNotFoundError:
        pass

for i in range(4, 2670):
    try:
        with open(f'.\htl_del_4000\\pos\\pos.{i}.txt', encoding='GBK', errors='ignore') as f2:
            for sentence in f2:
                sentence = set(jieba.lcut(sentence.strip()))
                for word in sentence:
                    if word not in word_fre:
                        word_fre[word] = 1
                    else:
                        word_fre[word] += 1
    except FileNotFoundError:
        pass

sentence_vec = []
tfidf_wight = []
for word in sentence_input:
    if word in model.wv:
        sentence_vec.append(model.wv[word].tolist())
    else:
        sentence_vec.append([0] * 64)
    fre = 0
    if word in word_fre:
        fre = word_fre[word]
    tfidf_wight.append((sentence_input.count(word) / len(sentence_input)) * log(4000 / (fre + 1)))

tfidf_wight = torch.tensor(numpy.array(tfidf_wight))
sentence_vec = torch.tensor(sentence_vec)
TFIDF_wight = torch.softmax(tfidf_wight, dim=0)
tfidf_wight = []
for num in TFIDF_wight:
    tfidf_wight.append([num])
tfidf_wight = torch.tensor(tfidf_wight)
output = (tfidf_wight * sentence_vec).sum(dim=0).tolist()

output = [output]
pre = Log_model.predict(output)
if pre == 0:
    print("该句为负面评论")
else:
    print("该句为正面评论")
