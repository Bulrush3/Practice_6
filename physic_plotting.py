import pandas as pd
import json
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

pd.set_option("display.max_rows", 20, "display.max_columns", 60)

def read_file(file_name):
    return pd.read_csv(file_name)

def read_types(file_name):
    dtypes = {}
    with open(file_name, mode="r") as file:
        dtypes = json.load(file)

    for key in dtypes.keys():
        if dtypes[key] == 'category':
            dtypes[key] = pd.CategoricalDtype
        else:
            dtypes[key] = np.dtype(dtypes[key])

    return dtypes

need_types = read_types('data/physic_data/dtypes.json') # не получилось использовать need_types как параметр dtype в методе read_csv
dataset = pd.read_csv("data/physic_data/df.csv", usecols=lambda x: x in need_types.keys())

print(dataset.columns)
dataset['activityID'] = dataset['activityID'].astype('category')
dataset['heart_rate'] = dataset['heart_rate'].astype('float32')
dataset['ankle magnetometer X'] = dataset['ankle magnetometer X'].astype('float32')
dataset['ankle magnetometer Y'] = dataset['ankle magnetometer Y'].astype('float32')
dataset['ankle magnetometer Z'] = dataset['ankle magnetometer Z'].astype('float32')
dataset['chest gyroscope X'] = dataset['chest gyroscope X'].astype('float32')
dataset['chest gyroscope Y'] = dataset['chest gyroscope Y'].astype('float32')
dataset['chest gyroscope Z'] = dataset['chest gyroscope Z'].astype('float32')

print(dataset.info(memory_usage='deep'))

# # График 1. Построение тепловой карты для числовых столбцов
# numerical_df = dataset.select_dtypes(include=['float32'])
# plt.figure(figsize=(10, 8))
# heatmap = sns.heatmap(numerical_df.corr(), annot=True, cmap='coolwarm', fmt='.2f')
# plt.title('Correlation Heatmap')
# heatmap.get_figure().savefig("data/physic_data/plots/plot1.png") 

  # # 1. Линейный график
# plt.figure(figsize=(10, 6))
# for activity, group in dataset.groupby('activityID'):
#     plt.plot(group['heart_rate'], label=activity, marker='o') 
# plt.xlabel('Время')
# plt.ylabel('Пульс')
# plt.title('Изменение пульса во времени')
# plt.legend() 
# plt.grid(True)  
# plt.savefig("data/physic_data/plots/plot2.png") 

# График круговой диаграммы
# plt.figure(figsize=(8, 6))
# dataset['activityID'].value_counts().plot(kind='pie', autopct='%1.1f%%')
# plt.ylabel('')
# plt.title('')
# plt.savefig("data/physic_data/plots/plot3.png")

# Гистограмма для heart rate
plt.figure(figsize=(8, 6))
sns.histplot(data=dataset, x='heart_rate', bins=20)
plt.xlabel('Пульс')
plt.ylabel('Частота')
plt.title('Распределение Пульса')
plt.savefig("data/physic_data/plots/plot4.png")

# Scatter plot для ankle magnetometer Y и ankle magnetometer Z
plt.figure(figsize=(8, 6))
sns.scatterplot(data=dataset, x='ankle magnetometer Y', y='ankle magnetometer Z', hue='activityID')
plt.xlabel('Магнитометр Y')
plt.ylabel('Магнитометр Z')
plt.title('Связь Магнитометра Y и Z')
plt.savefig("data/physic_data/plots/plot5.png")