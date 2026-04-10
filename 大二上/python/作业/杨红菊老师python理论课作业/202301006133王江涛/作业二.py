#随机生成10000个由大小写字母、数字、标点符号等组成字符串，统计出现的所有字符出现的个数。
import random
import string
import collections

# 生成随机字符串
def generate(length):
    char = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(char) for _ in range(length))

# 生成10000个随机字符串
random_strings = [generate(10000)]

# 将所有字符串合并成一个字符串
combined_string = ''.join(random_strings)

# 统计字符出现的个数
char_count = collections.Counter(combined_string)

# 打印结果
for char, count in char_count.items():
    print(f"'{char}': {count}")