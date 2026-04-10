people = [
    {"name": "张三", "visited_cities": ["北京", "上海", "广州"]},
    {"name": "李四", "visited_cities": ["深圳", "上海"]},
    {"name": "王五", "visited_cities": ["北京", "广州"]},
    {"name": "赵六", "visited_cities": ["上海", "杭州"]}]

for person in people:
    print(person["name"] + "去过{}个城市".format(len(person["visited_cities"])))
#如果输入的不是上述城市，则重新输入，输入后换行
while True:
    city = input("输入“北京”、“深圳”、“上海”、“杭州”、“广州”中的一个城市\n")
    if city in ["北京", "深圳", "上海", "杭州", "广州"]:
        break
    else:
        print("输入有误，请重新输入")
print("去过{}的人有{}个，分别是{}".format(city, len([person for person in people if city in person["visited_cities"]]),
                                 ", ".join(person["name"] for person in people if city in person["visited_cities"])))