import codecs
import numpy as np
import pandas as pd

PAI = {}
A = {}
B = {}
ww = {}
pos = []
frep = {}
frew = {}
fin = codecs.open("词性标注.txt", "r", "utf8")

for line in fin.readlines():
    temp = line.strip().split(" ")
    for i in range(0, len(temp)):
        word = temp[i].split("/")
        if len(word) == 2:
            if word[0] not in ww:
                ww[word[0]] = 1

            if word[1] not in pos:
                pos.append(word[1])
fin.close()
ww = ww.keys()

for i in pos:
    PAI[i] = 0
    frep[i] = 0
    A[i] = {}
    B[i] = {}

    for j in pos:
        A[i][j] = 0
    for j in ww:
        B[i][j] = 0

for w in ww:
    frew[w] = 1
line_num = 0
fin = codecs.open("train.txt", "r", "utf8")
for line in fin.readlines():
    if line == "\n":
        continue
    tmp = line.strip().split(" ")
    n = len(tmp)
    line_num += 1

    for i in range(1, n):

        word = tmp[i].split("/")
        pre = tmp[i - 1].split("/")
        if len(word) == 2 and len(pre) == 2:
            frew[word[0]] += 1
            frep[word[1]] += 1
            if i == 1:
                PAI[pre[1]] += 1
            else:
                A[pre[1]][word[1]] += 1
            B[word[1]][word[0]] += 1

for i in pos:
    PAI[i] = float(PAI[i]) / line_num

    for j in pos:
        if A[i][j] == 0:
            A[i][j] = 0.0001

    for j in ww:
        if B[i][j] == 0:
            B[i][j] = 0.0001
for i in pos:

    for j in pos:
        if frep[i] == 0:
            A[i][j] = 0
            continue
        A[i][j] = float(A[i][j]) / (frep[i])

    for j in ww:
        B[i][j] = float(B[i][j]) / (frew[j])
print(pd.DataFrame(B))
print(pd.DataFrame(A))
print(PAI)


# viterbi算法
def viterbi(a, b, pi, str_token, pos):
    # dp = {}
    # 计算文本长度
    num = len(str_token)
    # 绘制概率转移路径
    dp = [{} for i in range(0, num)]
    # 状态转移路径
    pre = [{} for i in range(0, num)]
    for k in pos:
        for j in range(num):
            dp[j][k] = 0
            pre[j][k] = ''
    # 句子初始化状态概率分布（首个词在所有词性的概率分布）
    for p in pos:

        if b[p][str_token[0]] is not None:
            dp[0][p] = pi[p] * b[p][str_token[0]] * 1000
        else:
            dp[0][p] = pi[p] * 0.0001 * 1000

    for i in range(0, num):
        for j in pos:
            if b[p][str_token[0]] is not None:
                sep = b[j][str_token[i]] * 1000
            else:
                # 计算发射概率,这个词不存在，应该置0.5/frew[str_token[i]]，这里默认为1
                sep = 0.0001 * 1000

            for k in pos:
                # 计算本step i 的状态是j的最佳概率和step i-1的最佳状态k(计算结果为step i 所有可能状态的最佳概率与其对应step i-1的最优状态)
                #
                if dp[i][j] < dp[i - 1][k] * a[k][j] * sep:
                    dp[i][j] = dp[i - 1][k] * a[k][j] * sep
                    # 各个step最优状态转移路径
                    pre[i][j] = k

    resp = {}
    #
    max_state = ""
    # 首先找到最后输出的最大观测值的状态设置为max_state
    for j in pos:
        if max_state == "" or dp[num - 1][j] > dp[num - 1][max_state]:
            max_state = j
    # print

    i = num - 1
    # 根据最大观测值max_state和前面求的pre找到概率最大的一条。
    while i >= 0:
        resp[i] = max_state
        max_state = pre[i][max_state]
        i -= 1
    return resp


with open('test.txt', 'r', encoding='utf8') as fin2:
    n_correct = 0
    n_total = 0

    for line in fin2.readlines():
        sentence = []
        right_sequence = []
        temp = line.strip().split(" ")
        for i in range(0, len(temp)):
            word = temp[i].split("/")
            if len(word) == 2:
                sentence.append(word[0])
                right_sequence.append(word[1])
        my_sequence = viterbi(A, B, PAI, sentence, pos)
        for i in range(0, len(right_sequence)):
            if right_sequence[i] == my_sequence[i]:
                n_correct += 1
        n_total += len(right_sequence)
    print(f"正确率为：{n_correct / n_total *100}%")
