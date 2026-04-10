import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

data = {
    'City': ['Hebei', 'Shanghai', 'Guilin', 'Henan', 'Shanxi'],
    'PM2.5': [85, 65, 55, 50, 215],
    'PM10': [120, 85, 70, 60, 140],
    'NO2': [40, 35, 30, 25, 50]
}
df = pd.DataFrame(data)
print("空气质量数据：")
print(df)

mean_pm25 = np.mean(df['PM2.5'])
std_pm25 = np.std(df['PM2.5'])

print(f"\n平均PM2.5值: {mean_pm25:.2f}")
print(f"PM2.5标准差: {std_pm25:.2f}")

df['AQI'] = (df['PM2.5'] + df['PM10'] + df['NO2']) / 3

print("\n空气质量指数（AQI）数据：")
print(df)

high_pollution_cities = df[df['PM2.5'] > 70]
print("\n高污染城市：")
print(high_pollution_cities)

plt.figure(figsize=(10,6))
plt.style.use('seaborn-v0_8-whitegrid')
plt.bar(df['City'],df['AQI'],color='b',alpha=0.7)
plt.xlabel('城市',fontsize=14)
plt.ylabel('空气质量指数（AQI）', fontsize=14)
plt.title('不同城市的空气质量指数（AQI）', fontsize=16)
plt.xticks(rotation=45)
plt.rcParams['font.sans-serif'] = ['SimHei']

for i, aqi in enumerate(df['AQI']):
    plt.text(i, aqi + 1, f'{aqi:.1f}', ha='center')


plt.savefig('aqi_analysis.png')
plt.show()



health_data = {
    'Region': ['North', 'South', 'East', 'West', 'Central'],
    'Diabetes_Prevalence': [8.1, 7.5, 9.0, 6.8, 7.9],
    'Population': [1200000, 800000, 1500000, 1000000, 1300000]
}


df_health = pd.DataFrame(health_data)


print("\n糖尿病患病率数据：")
print(df_health)


weighted_avg_diabetes=np.average(df_health['Diabetes_Prevalence'],weights=df_health['Population'])
print(f"\n加权平均糖尿病患病率: {weighted_avg_diabetes:.2f}")


plt.figure(figsize=(8, 5))   
plt.bar(df_health['Region'], df_health['Diabetes_Prevalence'], color='g', alpha=0.7)

plt.xlabel('地区', fontsize=14)
plt.ylabel('糖尿病患病率（%）', fontsize=14)
plt.title('不同地区的糖尿病患病率', fontsize=16)
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.xticks(rotation=45)  

for i, rate in enumerate(df_health['Diabetes_Prevalence']):
    plt.text(i, rate + 0.1, f'{rate:.1f}%', ha='center')

plt.savefig('diabetes_prevalence.png')
plt.show()


chunksize = 10000 
chunk_list = []  
for chunk in pd.read_csv('large_data.csv', chunksize=chunksize):
    chunk['column_of_interest'] = chunk['column_of_interest'].astype('float32') 
    chunk_list.append(chunk)

df_large = pd.concat(chunk_list)
print(df_large.info())
