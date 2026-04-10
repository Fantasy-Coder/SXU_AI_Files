import json
import pandas as pd
# 读取文本文件中的JSON数据
with open('E:\Python code\project\电影.txt', 'r', encoding='utf-8-sig') as file:
    data = json.load(file)

# 将JSON数据转换为DataFrame
df = pd.DataFrame(data)
# print(df)
# 将DataFrame保存为Excel文件
df.to_excel('E:\Python code\project\电影.xlsx', index=False,engine='openpyxl')

print("数据已成功保存为电影.xlsx")