from math import log, sqrt
import numpy as np
import jieba


dicts = {}
dic = {}
sentences = {}
stopwords = []
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


with open("句子向量表示（文档频率）.txt", 'r', encoding='utf8') as f3:
    for sentence in f3:
        sentence = sentence.strip().split("\t")
        if sentence[0] not in sentences:
            sentences[sentence[0]] = np.array(eval(sentence[1]))
    MyComment = "特别的好，尤其是前台的服务和解答！酒店位置也非常好，出门就是地铁。吃住出行还有游玩也都是步行的距离！强烈推荐！！！"
    MyComment = jieba.lcut(MyComment.strip())
    count = 0
    MyComment_vec = [0] * num
    for word, fre in dic.items():
        if word in MyComment:
            MyComment_vec[count] = (MyComment.count(word) / len(MyComment)) * log(4000 / (fre + 1))
        count += 1
    MyComment_vec = np.array(MyComment_vec)
    max_sim = {}
    flag = 0
    for id, vec in sentences.items():
        sim = np.dot(vec, MyComment_vec) / (sqrt(np.dot(vec, vec)) * sqrt(np.dot(MyComment_vec, MyComment_vec)))
        if flag < 3:
            max_sim[id] = sim
            flag += 1
        elif sim > max_sim[min(max_sim, key=max_sim.get)]:
            max_sim.pop(min(max_sim, key=max_sim.get))
            max_sim[id] = sim
    for id, sim in max_sim.items():
        print(f"序号为{id}， 相似度为{sim}\n")
