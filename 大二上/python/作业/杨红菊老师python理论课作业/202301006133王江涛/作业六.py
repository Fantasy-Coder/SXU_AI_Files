import pandas as pd
import faker
fake = faker.Faker('zh_CN')
data = {
    "姓名": [],
    "电话": [],
    "公司": [],
    "邮箱": [],
    "年龄": [],
    "性别": []
}

for i in range(100):
    data["姓名"].append(fake.name())
    data["电话"].append(fake.phone_number())
    data["公司"].append(fake.company())
    data["邮箱"].append(fake.email())
    data["年龄"].append(fake.random_int(min=20, max=50))
    data["性别"].append(fake.random_element(elements=('男', '女')))
df = pd.DataFrame(data)
df.to_excel('E:\Python code\project\名单.xlsx', index=False)


