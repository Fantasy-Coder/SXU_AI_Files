import jieba

dicts = {}
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
                if sentence_to_cut == "\n":
                    continue
                sentence = jieba.lcut(sentence_to_cut.strip())
                sentence = set(sentence)
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
        continue

# 特征排序
dics = sorted(dicts.items(), key=lambda x: x[1])

# 选择写入文件的特征词
with open('特征词.txt', 'w', encoding='utf8') as f3:
    for i in range(len(dics) - 2000, len(dics) - 1000):
        word, fre = dics[i]
        f3.write(f"{word}\t{fre}\n")

