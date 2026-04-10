import gensim.models as word2vec
import jieba
import numpy as np
import torch

model = word2vec.Word2Vec.load("Skip-Gram.model")
All_sentence_vec = []

for i in range(0, 2670):
    try:
        with open(f'.\htl_del_4000\\neg\\neg.{i}.txt', encoding='GBK', errors='ignore') as f1:
            sentence = []
            for line in f1:
                if line == "\n":
                    continue
                for j in jieba.lcut(line.strip()):
                    sentence.append(model.wv[j].tolist())
            All_sentence_vec.append(sentence)
    except FileNotFoundError:
        pass

for i in range(4, 2670):
    try:
        with open(f'.\htl_del_4000\\pos\\pos.{i}.txt', encoding='GBK', errors='ignore') as f2:
            sentence = []
            for line in f2:
                if line == "\n":
                    continue
                for j in jieba.lcut(line.strip()):
                    sentence.append(model.wv[j].tolist())
            All_sentence_vec.append(sentence)
    except FileNotFoundError:
        pass

All_sentence_tfidf = []
All_sentence_id = []
with open("句子向量表示.txt", 'r', encoding="utf8") as f3:
    for line in f3:
        tfidf = list(eval(line.strip().split('\t')[1]))
        sentence_id = line.strip().split('\t')[0]
        All_sentence_id.append(sentence_id)
        All_sentence_tfidf.append(tfidf)

with open("实验七.txt", 'w', encoding='utf8') as f4:
    for i in range(0, len(All_sentence_tfidf)):
        sentence_id = All_sentence_id[i]
        sentence_class = sentence_id[0:3]
        if sentence_class == "neg":
            sentence_class = 0
        else:
            sentence_class = 1
        sentence_tfidf = torch.tensor(np.array(All_sentence_tfidf[i]))
        TFIDF_wight = torch.softmax(sentence_tfidf, dim=0)
        tfidf_wight = []
        for num in TFIDF_wight:
            tfidf_wight.append([num])
        tfidf_wight = torch.tensor(tfidf_wight)
        sentence_vec = torch.tensor(All_sentence_vec[i])
        output = (tfidf_wight * sentence_vec).sum(dim=0).tolist()
        f4.write(f"{sentence_id}\t{sentence_class}\t{output}\n")
