import csv
import gensim
import jieba
import numpy as np
import os

from gensim.models import word2vec

content = open('./cn_stopwords.txt', 'r', encoding='utf-8').read()


# 转化为CSV文件
def ToCSV(file1, file2):
    with open(file1, 'w', newline='', encoding='utf-8') as cf:
        writer = csv.writer(cf)
        writer.writerow(["id", "标签", "向量"])
        with open(file2, 'r', encoding='utf-8') as f:
            l = f.readlines()
            for s in l:
                l1 = s.split(' ')  # l1[0]为文档id,l1[1]为标签，l1[2:]为向量
                writer.writerow([l1[0], l1[1], l1[2:]])


def funn():  # 对给定的数据进行分词
    # 当前文件的路径
    dir = os.path.dirname(__file__)
    # 拼接文件路径
    neg_folder = os.path.join(dir, './htl_del_4000/' + "neg")
    pos_folder = os.path.join(dir, './htl_del_4000/' + "pos")
    # 遍历所有文件
    neg_li = os.listdir(neg_folder)  # li储存neg的句子文本
    pos_li = os.listdir(pos_folder)  # li_1储存pos的句子文本
    with open("./临时.txt", "w+", encoding="utf-8") as file:
        num_neg = 0
        num_pos = 0
        for x in neg_li:
            with open("./htl_del_4000/neg/" + x, "r", encoding="gbk", errors='ignore') as f:
                content = f.read()
                num_neg += 1
                words = []
                # words=jieba.cut(content)
                words_split = " ".join(jieba.cut(content)).split()
                # words=" ".join(words_split)
                for w in words_split:
                    # if w not in stop_words:
                    words.append(w)
                words = " ".join(words)
                # print(words)
                file.writelines(words + "\n")
        for x in pos_li:
            with open("./htl_del_4000/pos/" + x, "r", encoding="gbk", errors='ignore') as f:
                content = f.read()
                num_pos += 1
                words = []
                # words=jieba.cut(content)
                words_split = " ".join(jieba.cut(content)).split()
                # words=" ".join(words_split)
                for w in words_split:
                    # if w not in stop_words: #不去除停用词可以注释掉
                    words.append(w)
                words = " ".join(words)
                # print(words)
                file.writelines(words + "\n")
    return num_neg, num_pos


def Get_WordVector():
    # 用word2vec建立词向量
    sens = word2vec.LineSentence("./临时.txt")
    # sens:句子，min_count:词频小于设定值的词扔掉，window:一次取的词数，size:词向量的维度，sg:使用CBOW/Skip，hs:若为1采用树优化，worker:CPU并行数量，iter:最大迭代次数
    model_CBOW = gensim.models.word2vec.Word2Vec(sens, min_count=0, window=5, vector_size=64, sg=0, hs=0, negative=5,
                                                 workers=8, epochs=200)  # 用CBOW处理
    model_skipgram = gensim.models.word2vec.Word2Vec(sens, min_count=0, window=5, vector_size=64, sg=1, hs=0,
                                                     negative=5, workers=8, epochs=200)  # 用skip-gram处理
    # 保存为txt
    model_CBOW.wv.save_word2vec_format("词向量(cbow).txt", binary=False)
    model_skipgram.wv.save_word2vec_format("词向量(skip-gram).txt", binary=False)


def calw(docs):
    tfidf = []
    words_stats = {}
    docs_num = len(docs)
    for ws in docs:  # ws=sentense
        for w in ws:  # w=words
            if w not in words_stats:
                words_stats[w] = {}
                words_stats[w]['df'] = 0
                words_stats[w]['idf'] = 0
            # words_stats[w]['cf'] += 1
        for w in set(ws):
            words_stats[w]['df'] += 1
    for w, winfo in words_stats.items():
        words_stats[w]['idf'] = np.log((1. + docs_num) / (1. + winfo['df']))
        tfidf.append(words_stats[w]['idf'])
    return tfidf


def ca(docs):
    tfidf = []
    words_stats = {}
    docs_num = len(docs)
    for ws in docs:  # ws=sentense
        for w in ws:  # w=words
            w = ''
    return tfidf


# softmax归一化函数
def softmax(x):
    e_x = np.exp(x)
    return e_x / e_x.sum()


def final():
    docs = []
    num_of_files = 0
    for x in l1:  # 文件挨个计算
        with open("./htl_del_4000/neg/" + x, "r", encoding="gbk", errors='ignore') as f:
            content = f.read()
            words = jieba.cut(content)
            num_sentense = 0
            temp_doc = [x.replace(".", '').replace('neg', '').replace('txt', '') + "-" + str(num_sentense),
                        "0"]  # 1表示pos;0表示neg（num_sentense的0表示该文档下的第一个句子）
            for i in words:
                if i == "。" or i == "；" or i == ".":
                    num_sentense += 1
                    temp_doc.append(i)
                    docs.append(temp_doc)
                    temp_doc = [x.replace(".", '').replace('neg', '').replace('txt', '') + "-" + str(num_sentense), "0"]
                    num_of_files += 1
                    continue
                elif i != "\r" and i != "\r\n" and i != "\n":
                    temp_doc.append(i)
            else:
                if len(temp_doc) > 3:
                    docs.append(temp_doc)
                    num_of_files += 1
    num_of_files_1 = 0
    for x in l2:
        with open("./htl_del_4000/pos/" + x, "r", encoding="gbk", errors='ignore') as f1:
            content = f1.read()
            words = jieba.cut(content)
            num_sentense = 0
            temp_doc = [x.replace(".", '').replace('pos', '').replace('txt', '') + "-" + str(num_sentense),
                        "1"]  # 1表示pos;0表示neg（num_sentense的0表示该文档下的第一个句子）
            for i in words:
                if i == "。" or i == ";" or i == ".":
                    num_sentense += 1
                    temp_doc.append(i)
                    docs.append(temp_doc)
                    temp_doc = [x.replace(".", '').replace('pos', '').replace('txt', '') + "-" + str(num_sentense), "1"]
                    num_of_files_1 += 1
                    continue
                elif i != "\r" and i != "\r\n" and i != "\n":
                    temp_doc.append(i)
            else:
                if len(temp_doc) > 3:
                    docs.append(temp_doc)
                    num_of_files_1 += 1
    return docs


def prosm(sen_docs, file):
    tfidf = []
    for sentense in sen_docs:
        if len(sentense) < 4:  # 因为文档中有"..."出现，所以上一步会有空列表出现，这一步把他们都去掉
            continue
        x = calw(sentense[2:])
        res = softmax(x)
        tfidf.append(sentense[:2] + (res * np.array(x)).tolist())  # (res * np.array(x)).tolist()加权求和得到句子的表示向量
    with open(file, "w+", encoding="utf-8") as f:
        for sentense in range(len(tfidf)):
            for value in range(len(tfidf[sentense])):
                f.write(str(tfidf[sentense][value]))
                if (value != (len(tfidf[sentense]) - 1)):
                    f.write(' ')
            f.write('\n')


if __name__ == "__main__":
    funn()
    Get_WordVector()  # 建立词向量
    # 将数据加载到列表
    fname1 = 'neg'
    fname2 = 'pos'
    # 当前文件的路径
    dir = os.path.dirname(__file__)
    x = 200
    softmax(x)
    # 拼接文件路径
    f1 = os.path.join(dir, './htl_del_4000/' + fname1)
    f2 = os.path.join(dir, './htl_del_4000/', fname2)
    # 遍历所有文件
    l1 = os.listdir(f1)  # l1储存neg的句子文本
    l2 = os.listdir(f2)  # l2储存pos的句子文本
    l1.sort()
    l2.sort()
    docs = final()
    calw(docs)
    ca(docs)
    prosm(docs, "表示.txt")
    ToCSV("Word2Vec.csv", "表示.txt")
    print("任务完成！")

model = load_word2vec_model("Skip-Gram.model")
print(model.wv["好评"].tolist())
