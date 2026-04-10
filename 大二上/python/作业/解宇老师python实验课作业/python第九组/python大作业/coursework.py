import numpy as np
import pandas as pd
import requests
import time
import seaborn as sns
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import pickle
import tkinter as tk
import tkinter.messagebox

window = tk.Tk()
window.title('Welcome')
window.geometry('450x300')
canvas = tk.Canvas(window, height=300, width=450)
image_file = tk.PhotoImage(file='welcome1.gif')
image = canvas.create_image(0, 0, anchor='nw', image=image_file)
canvas.pack(side='top')
tk.Label(window, text='用户名').place(x=100, y=90)
tk.Label(window, text='密码').place(x=100, y=140)

var_usr_name = tk.StringVar()
var_usr_name.set('请输入您的姓名')
entry_usr_name = tk.Entry(window, textvariable=var_usr_name)
entry_usr_name.place(x=210, y=90)

var_usr_pwd = tk.StringVar()
entry_usr_pwd = tk.Entry(window, textvariable=var_usr_pwd, show='*')
entry_usr_pwd.place(x=210, y=140)

def usr_login():
    usr_name = var_usr_name.get()
    usr_pwd = var_usr_pwd.get
#开始一个try-except块，用于处理文件不存在的情况。
    try:
        #尝试以二进制读取模式打开一个名为usrs_info.pickle的文件。这个文件应该包含用户的登录信息。
        with open("usrs_info.pickle", "rb") as usr_file:
            print("1")
            usrs_info = pickle.load(usr_file)
            print(usrs_info)
#如果文件不存在，则执行except块中的代码。
    except FileNotFoundError:
        #以二进制写入模式打开同一个文件。如果文件不存在，它将被创建。
        with open("usrs_info.pickle", "wb") as usr_file:
            print("2")
            usrs_info = {"admin": "admin"}
            pickle.dump(usrs_info, usr_file)

    if usr_name in usrs_info:
        print("3")
        if usr_pwd == usrs_info[usr_name]:
            tk.messagebox.showinfo(title="Welcome", message="亲爱的 " + usr_name)
        else:
            tk.messagebox.showerror(message="密码错误，请重试")
    else:
        print("4")
        is_sign_up = tk.messagebox.askyesno(title="Welcome", message="账号不存在，是否注册账号？")
        if is_sign_up:
            usr_sign_up()

def usr_sign_up():
    print("注册开始")

    def sign_up():
        nn = input_entry1.get()
        np = input_entry2.get()
        npf = input_entry3.get()
        # 读取后台数据
        with open("usrs_info.pickle", "rb") as usr_file:
            exist_usr_info = pickle.load(usr_file)
        #
        if np != npf:
            tk.messagebox.showerror("错误","两次密码输入不一样")

        elif nn in exist_usr_info:
            print("已经注册过了")
            tk.messagebox.showerror("错误，用户已存在")

        else:
            exist_usr_info[nn] = np
            with open("usrs_info.pickle", "wb") as usr_file:
                pickle.dump(exist_usr_info, usr_file)

            tk.messagebox.showinfo("提示","注册成功")

            # 销毁窗口
            root.destroy()

    root = tk.Tk()
    root.title("Sign up window")
    root.geometry("350x200")

    # 设置标签和输入框
    tk.Label(root, text=" ").grid(row=1, column=0, sticky='e', padx=10, pady=5)
    tk.Label(root, text="用户名").grid(row=2, column=0, sticky='e', padx=10, pady=5)
    input_entry1 = tk.Entry(root)
    input_entry1.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(root, text="密码").grid(row=3, column=0, sticky='e', padx=10, pady=5)
    input_entry2 = tk.Entry(root, show='*')
    input_entry2.grid(row=3, column=1, padx=10, pady=5)

    tk.Label(root, text="确认密码").grid(row=4, column=0, sticky='e', padx=10, pady=5)
    input_entry3 = tk.Entry(root, show='*')
    input_entry3.grid(row=4, column=1, padx=10, pady=5)

    # 设置按钮
    signup_button = tk.Button(root, text="注册", command=sign_up)
    signup_button.grid(row=5, column=1, columnspan=1, padx=10, pady=5)

btn_login = tk.Button(window, text='登录', command=usr_login)
btn_login.place(x=130, y=210)
btn_sign_up = tk.Button(window, text='注册', command=usr_sign_up)
btn_sign_up.place(x=230, y=210)

window.mainloop()
#
headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
        (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'}
def get_areas(url):
    try:
        print('start grabing areas')
        response = requests.get(url, headers=headers, timeout=30)
        html = response.content
        soup = BeautifulSoup(html, 'html.parser')

        all_sights = soup.findAll('li', 'filter__item--level2')
        print(all_sights)
        areas = []
        areas_links = []
        for item in all_sights:
            if not item.get_text()=='\n不限\n':
                areas.append(item.get_text())
                areas_links.append('https://ty.zu.anjuke.com/'+item.find('a').get('href'))

        return areas, areas_links

    except Exception as e:
        print('爬取网站出现了一点问题，问题如下：')
        print(e)
        return ''
def get_pages(area, area_link):
    print("开始抓取页面")
    response = requests.get(area_link, headers=headers)
    html = response.content
    soup = BeautifulSoup(html, 'html.parser')
    pages = int(soup.findAll('div', 'page-content')[0].get('multi-page'))
    print("这个区域有" + str(pages) + "页")
    info = []
    for page in range(1,pages+1):
        url = 'https://ty.anjuke.com/community/xiaodiana' + str(page)
        print("\r开始抓取%s页的信息, 已爬取%s条数据"%(str(page), len(info)), end='')
        info += get_house_info(area, url)
    return info
def get_house_info(area, url, info=[]):
    try:
        response = requests.get(url, headers=headers)
        html = response.content
        soup = BeautifulSoup(html, 'html.parser')

        all_text = soup.findAll('div', 'content__list--item')

        for item in all_text:
            item = item.get_text()
            item = item.replace(' ', '').split('\n')
            while "" in item:
                item.remove("")
            while "/" in item:
                item.remove("/")
            info.append(item)
        return info

    except Exception as e:
        print(e)
        time.sleep(2)
        return get_house_info(area, url)
info = []
url = 'https://ty.anjuke.com/community/xiaodiana'
areas, area_link = get_areas(url)
info = get_pages(areas[1], area_link[1])
def keys(info, key=''):
    ls = []
    for item in info:
        if key in item:
            ls.append(key)
        else:
            ls.append('')
    return ls
# 步骤7： 数据清洗：清洗数据，并保存为csv文件
def clean_data(info, key=''):
    title = [item[0] for item in info]
    address = [item[1] for item in info]
    area = [item[2] for item in info]
    toward = [item[3] for item in info]
    style = [item[4] for item in info]
    floor = [item[5] for item in info]

    source = [item[6] for item in info]
    time = [item[7] for item in info]
    price = [item[-1] for item in info]

    subway = keys(info, '近地铁')
    decorate = keys(info, '精装')
    heating = keys(info, '集中供暖')
    new_room = keys(info, '新上')
    time_for_look = keys(info, '随时看房')
    return pd.DataFrame({
        'title': title,
        'address': address,
        'area': area,
        'toward': toward,
        'style': style,
        'floor': floor,
        'source': source,
        'time': time,
        'price': price,
        'subway': subway,
        'decorate': decorate,
        'heating': heating,
        'new_room': new_room,
        'time_for_look': time_for_look
        })

data = clean_data(info)
data.to_csv('data.csv', index=True)
#步骤8：读取已爬取的数据，并对数据进行数字化
data = pd.read_csv('./data.csv')
# 客厅数量
data['sitting_room_value'] = data['style'].apply(lambda x: x.split('厅')[0][-1])
data['sitting_room_value'] = data['sitting_room_value'].replace('卫', 0)
# 卧室浴室数量
data['bedroom_value'] = data['style'].apply(lambda x: x[0])
data['bathroom_value'] = data['style'].apply(lambda x: x[-2])
# 价格、面积、楼层
data['price_value'] = data['price'].apply(lambda x: x[:-3])
data['area_value'] = data['area'].apply(lambda x: x[:-1])
data['floor_value'] = data['floor'].apply(lambda x: x.split('（')[-1][0])
# 租房方位朝向
def toward(x, key=''):
    if key in x:
        return key
    else:
        return 0
data['north'] = data['toward'].apply(lambda x: toward(x, '北')).replace('北', 1)
data['south'] = data['toward'].apply(lambda x: toward(x, '南')).replace('南', 1)
data['east'] = data['toward'].apply(lambda x: toward(x, '东')).replace('东', 1)
data['west'] = data['toward'].apply(lambda x: toward(x, '西')).replace('西', 1)
# 提取全部的数值数据
values_data = data[['sitting_room_value', 'bedroom_value',
                    'bathroom_value', 'price_value', 'area_value',
                    'floor_value', 'north',
                    'south', 'east', 'west']].astype(float)
# 描述性统计
values_data.describe()
#分析价格分布
sns.histplot(values_data['price_value'], kde=True)

#由于分析过程相同，只展示价格与面积的关系
sns.jointplot(x='area_value', y='price_value', data=values_data)

#分析各因素之间可能存在的关系
sns.pairplot(values_data)
mod = smf.quantreg('price_value ~ area_value', values_data)
res = mod.fit(q=.5)

quantiles = np.arange(.05, .96, .1)
def fit_model(q):
    res = mod.fit(q=q)
    return [q, res.params['Intercept'], res.params['area_value']] + \
            res.conf_int().loc['area_value'].tolist()

models = [fit_model(x) for x in quantiles]
models = pd.DataFrame(models, columns=['q', 'a', 'b', 'lb', 'ub'])

ols = smf.ols('price_value ~ area_value', values_data).fit()
ols_ci = ols.conf_int().loc['area_value'].tolist()
ols = dict(a = ols.params['Intercept'],
           b = ols.params['area_value'],
           lb = ols_ci[0],
           ub = ols_ci[1])

print(models)
print(ols)
x = np.arange(values_data.area_value.min(), values_data.area_value.max(), 50)
get_y = lambda a, b: a + b * x

fig, ax = plt.subplots(figsize=(8, 6))

for i in range(models.shape[0]):
    y = get_y(models.a[i], models.b[i])
    ax.plot(x, y, linestyle='dotted', color='grey')

y = get_y(ols['a'], ols['b'])

ax.plot(x, y, color='red', label='OLS')
ax.scatter(values_data.area_value, values_data.price_value, alpha=.2)

legend = ax.legend()
ax.set_xlabel('Area', fontsize=16)
ax.set_ylabel('Price', fontsize=16)
