from math import log

import jieba

stopwords = []
dicts = {}
dic = {}
num = 0

# 建立停用词表
with open('cn_stopwords.txt', encoding='utf8') as f0:
    for stopword in f0:
        stopwords.append(stopword.strip())

for i in range(0, 2670):
    try:
        with open(f'.\htl_del_4000\\neg\\neg.{i}.txt', encoding='GBK', errors='ignore') as f1:
            for sentence_to_cut in f1:
                sentence = jieba.lcut(sentence_to_cut.strip())
                for word in sentence:
                    if word in stopwords:
                        continue
                    if word not in dicts:
                        dicts[word] = 1
                    else:
                        dicts[word] += 1
    except FileNotFoundError:
        pass

for i in range(4, 2670):
    try:
        with open(f'.\htl_del_4000\\pos\\pos.{i}.txt', encoding='GBK', errors='ignore') as f2:
            for sentence_to_cut in f2:
                sentence = jieba.lcut(sentence_to_cut.strip())
                for word in sentence:
                    if word in stopwords:
                        continue
                    if word not in dicts:
                        dicts[word] = 1
                    else:
                        dicts[word] += 1
    except FileNotFoundError:
        pass

with open("互信息值.txt", 'r', encoding='utf8')as f3:
    for sentence in f3:
        sentence = sentence.strip().split(":")
        num += 1
        if sentence[0] not in dic:
            dic[sentence[0]] = dicts[sentence[0]]

with open("6.1句子向量表示（互信息）.txt", 'w', encoding='utf8') as f4:
    for i in range(0, 2670):
        try:
            with open(f'.\htl_del_4000\\neg\\neg.{i}.txt', encoding='GBK', errors='ignore') as f5:
                sentence = []
                count = 0
                sentence_vec = [0] * num
                for sentence_to_cut in f5:
                    if sentence_to_cut == "\n":
                        continue
                    sentence += jieba.lcut(sentence_to_cut.strip())
                for word, fre in dic.items():
                    if word in sentence:
                        sentence_vec[count] = (sentence.count(word) / len(sentence)) * log(4000 / (fre + 1))
                    count += 1
                f4.write(f"neg{i}\t{sentence_vec}\n")
        except FileNotFoundError:
            pass

    for i in range(4, 2670):
        try:
            with open(f'.\htl_del_4000\\pos\\pos.{i}.txt', encoding='GBK', errors='ignore') as f6:
                sentence = []
                count = 0
                sentence_vec = [0] * num
                for sentence_to_cut in f6:
                    if sentence_to_cut == "\n":
                        continue
                    sentence += jieba.lcut(sentence_to_cut.strip())
                for word, fre in dic.items():
                    if word in sentence:
                        sentence_vec[count] = (sentence.count(word) / len(sentence)) * log(4000 / (fre + 1))
                    count += 1
                f4.write(f"pos{i}\t{sentence_vec}\n")
        except FileNotFoundError:
            pass

