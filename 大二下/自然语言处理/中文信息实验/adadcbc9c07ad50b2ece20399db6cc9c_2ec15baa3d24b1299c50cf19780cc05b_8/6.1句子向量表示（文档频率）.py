import sys
from math import log
import jieba

dic = {}
num = 0

# 加载特征词集及包含该词的文档数
with open("特征词.txt", 'r', encoding="utf8") as f1:
    for words in f1:
        num += 1
        x = words.strip().split('\t')
        word = x[0]
        fre = int(x[1])
        if word not in dic:
            dic[word] = fre

# 构造句子的特征向量
with open("句子向量表示（文档频率）.txt", 'w', encoding='utf8') as f3:
    for i in range(0, 2670):
        try:
            with open(f'.\htl_del_4000\\neg\\neg.{i}.txt', encoding='GBK', errors='ignore') as f2:
                sentence = []
                count = 0
                sentence_vec = [0] * num
                for sentence_to_cut in f2:
                    if sentence_to_cut == "\n":
                        continue
                    sentence += jieba.lcut(sentence_to_cut.strip())
                for word, fre in dic.items():
                    if word in sentence:
                        sentence_vec[count] = (sentence.count(word) / len(sentence)) * log(4000 / (fre + 1))
                    count += 1
                f3.write(f"neg{i}\t{sentence_vec}\n")
        except FileNotFoundError:
            pass

    for i in range(4, 2670):
        try:
            with open(f'.\htl_del_4000\\pos\\pos.{i}.txt', encoding='GBK', errors='ignore') as f4:
                sentence = []
                count = 0
                sentence_vec = [0] * num
                for sentence_to_cut in f4:
                    if sentence_to_cut == "\n":
                        continue
                    sentence += jieba.lcut(sentence_to_cut.strip())
                for word, fre in dic.items():
                    if word in sentence:
                        sentence_vec[count] = (sentence.count(word) / len(sentence)) * log(4000 / (fre + 1))
                    count += 1
                f3.write(f"pos{i}\t{sentence_vec}\n")
        except FileNotFoundError:
            pass
