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

need_types = read_types('data/asteroid_data/dtypes.json') # не получилось использовать need_types как параметр dtype в методе read_csv
dataset = pd.read_csv("data/asteroid_data/df.csv", usecols=lambda x: x in need_types.keys())

dataset['spkid'] = dataset['spkid'].astype('uint32')
dataset['epoch_mjd'] = dataset['epoch_mjd'].astype('uint16')
dataset['H'] = dataset['H'].astype('float32')
dataset['diameter'] = dataset['diameter'].astype('float32')
dataset['diameter_sigma'] = dataset['diameter_sigma'].astype('float32')
dataset['rms'] = dataset['rms'].astype('float32')
dataset['full_name'] = dataset['full_name'].astype('object')
dataset['name'] = dataset['name'].astype('category')
dataset['orbit_id'] = dataset['orbit_id'].astype('category')
dataset['class'] = dataset['class'].astype('category')

print(dataset.info(memory_usage='deep'))

# Корреляционная матрица
# numerical_vars = ['H', 'diameter', 'diameter_sigma', 'rms', 'spkid', 'epoch_mjd']
# correlation_matrix = dataset[numerical_vars].corr()
# plt.figure(figsize=(8, 6))
# sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
# plt.title('Корреляционная матрица')
# plt.savefig('data/asteroid_data/plots/plot1.png')

# 2 Линейный график
# plt.figure(figsize=(8, 6))
# sns.lineplot(x='H', y='diameter_sigma', data=dataset)
# plt.xlabel('')
# plt.ylabel('')
# plt.title('')
# plt.savefig('data/asteroid_data/plots/plot2.png')

# График 3
# fig = plt.figure(figsize=(15,15))
# sns.pairplot(data = dataset.sample(100), hue ='diameter', 
#              palette = 'bwr',).savefig("data/asteroid_data/plots/plot3.png")


# График 4
# plt.figure(figsize=(20, 10))
# plot = dataset['class'].value_counts().loc[lambda x : x > 200].plot(kind='bar', title='class')
# plt.title("class")
# plot.figure.savefig("data/asteroid_data/plots/plot4.png")

# 5 
# plt.figure(figsize=(20, 10))
# plot = dataset['orbit_id'].value_counts().loc[lambda x : x > 3000].plot(kind='bar', title='class')
# plt.title("orbit_id")
# plot.figure.savefig("data/asteroid_data/plots/plot5.png")


