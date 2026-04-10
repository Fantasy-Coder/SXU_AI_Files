import pickle
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

content = []
label = []
with open("加权句子向量表示.txt", 'r', encoding='utf8')as f1:
    for sentence in f1:
        sentence = sentence.split('\t')
        content.append(list(eval(sentence[2])))
        label.append(int(sentence[1]))

train_data, test_data, train_labels, test_labels = train_test_split(content, label, test_size=0.2, random_state=42)

model = LogisticRegression(random_state=6).fit(train_data, train_labels)
print(model.score(test_data, test_labels))

TP, TN, FP, FN = 0, 0, 0, 0
pre = model.predict(test_data)
for i in range(0, len(pre)):
    if pre[i] == 1:
        if test_labels[i] == 1:
            TP += 1
        else:
            FP += 1
    else:
        if test_labels[i] == 0:
            TN += 1
        else:
            FN += 1

Accuracy = (TN + TP) / (TN + TP + FN + FP)
Recall = TP / (TP + FN)
F1 = 2 * TP / (2 * TP + FP + FN)

print(f"准确率为：{Accuracy}\n召回率为：{Recall}\nF1指标为{F1}")

with open("w2v_LogisticRegression_model.pickle", 'wb')as fout:
    pickle.dump(model, fout)