import jieba

vocab = {}
with open('CDIAL-BIAS-race.txt', 'r', encoding='utf8') as file:
    with open('output.txt', 'w', encoding='utf8') as outfile:
        file_userdict = 'race.txt'
        jieba.load_userdict(file_userdict)
        for line in file:
            line = line.strip()
            outfile.write("\n")
            for word in jieba.cut(line):
                if word in vocab:
                    vocab[word] += 1
                else:
                    vocab[word] = 1
                if word.isdigit():
                    continue
                outfile.write(word + "/")

with open('敏感词.txt', 'w', encoding='utf8') as outfile2:
    with open('race.txt', 'r', encoding='utf8') as file2:
        word = word.replace('\n', '')
        vocab2 = {}
        for word in file2:
            word = word.strip()
            if word in vocab:
                vocab2[word] = vocab[word]
            else:
                vocab2[word] = 0
        list1 = sorted(vocab2.items(), key=lambda x: x[1])
        for word, kkk in list1:
            if word in vocab:
                outfile2.write("{}: {}\n".format(word, vocab[word]))
            else:
                outfile2.write("{}: {}\n".format(word, 0))
