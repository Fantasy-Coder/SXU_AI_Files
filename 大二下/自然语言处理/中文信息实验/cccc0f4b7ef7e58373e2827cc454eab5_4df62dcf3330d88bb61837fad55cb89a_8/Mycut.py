import jieba

all_cut = []
max_size = 25


def cut(str1):
    length = len(str1)
    Word = str1
    Cut = []
    x = 0
    y = 0
    while length > 0:
        if len(Word) < max_size:
            now_Word = Word
        else:
            now_Word = Word[0:max_size]
        while now_Word not in dic:
            if len(now_Word) == 1:
                break
            now_Word = now_Word[0:len(now_Word) - 1]
        y = len(now_Word) + y
        Cut.append((x, y))
        Word = Word[len(now_Word):]
        x = x + len(now_Word)
        length = len(Word)
    return Cut


words = []
txt = "race.txt"
jieba.load_userdict(txt)

with open('jieba.txt', 'w', encoding='utf-8') as f2:
    with open('CDIAL-BIAS-race.txt', encoding='utf-8') as f1:
        a = str(f1.readline())
        while a:
            c = jieba.lcut(a)
            index = []
            j = 0
            for i in range(len(c)):
                tup = (j, j + len(c[i]))
                j = j + len(c[i])
                index.append(tup)
            f2.write(str(index) + '\n')
            a = str(f1.readline())

dic = []
with open('output.txt', 'r', encoding="utf8") as dics:
    for word in dics:
        dic.append(word.strip())

with open('CDIAL-BIAS-race.txt', 'r', encoding='utf-8') as f2:
    a = f2.readline()
    with open('mycut.txt', 'w', encoding='utf-8') as f3:
        while a:
            cuta = cut(a)
            a = f2.readline()
            f3.write(str(cuta) + '\n')


