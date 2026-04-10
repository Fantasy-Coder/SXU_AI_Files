from math import log
import jieba

dicts = {}

for i in range(0, 2670):
    try:
        with open(f'.\htl_del_4000\\neg\\neg.{i}.txt', encoding='GBK', errors='ignore') as f1:
            for sentence_to_cut in f1:
                sentence = jieba.lcut(sentence_to_cut.strip())
                for word in sentence:
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
                    if word not in dicts:
                        dicts[word] = 1
                    else:
                        dicts[word] += 1
    except FileNotFoundError:
        pass

with open("句子向量表示.txt", 'w', encoding='utf8') as f4:
    for i in range(0, 2670):
        try:
            with open(f'.\htl_del_4000\\neg\\neg.{i}.txt', encoding='GBK', errors='ignore') as f5:
                sentence = []
                sentence_vec = []
                for sentence_to_cut in f5:
                    if sentence_to_cut == "\n":
                        continue
                    sentence += jieba.lcut(sentence_to_cut.strip())
                for word in sentence:
                    if word in dicts:
                        fre = dicts[word]
                    else:
                        fre = 0
                    sentence_vec.append((sentence.count(word) / len(sentence)) * log(4000 / (fre + 1)))
                f4.write(f"neg{i}\t{sentence_vec}\n")
        except FileNotFoundError:
            pass

    for i in range(4, 2670):
        try:
            with open(f'.\htl_del_4000\\pos\\pos.{i}.txt', encoding='GBK', errors='ignore') as f6:
                sentence = []
                sentence_vec = []
                for sentence_to_cut in f6:
                    if sentence_to_cut == "\n":
                        continue
                    sentence += jieba.lcut(sentence_to_cut.strip())
                for word in sentence:
                    if word in dicts:
                        fre = dicts[word]
                    else:
                        fre = 0
                    sentence_vec.append((sentence.count(word) / len(sentence)) * log(4000 / (fre + 1)))
                f4.write(f"pos{i}\t{sentence_vec}\n")
        except FileNotFoundError:
            pass
