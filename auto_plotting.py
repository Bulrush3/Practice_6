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

need_types = read_types('data/auto_data/dtypes.json') # не получилось использовать need_types как параметр dtype в методе read_csv
dataset = pd.read_csv("data/auto_data/df.csv", usecols=lambda x: x in need_types.keys())
dataset['vin'] = dataset['vin'].astype('object')
dataset['msrp'] = dataset['msrp'].astype('uint32')
dataset['askPrice'] = dataset['askPrice'].astype('uint32')
dataset['mileage'] = dataset['mileage'].astype('uint32')
dataset['isNew'] = dataset['isNew'].astype('bool')
dataset['color'] = dataset['color'].astype('category')
dataset['interiorColor'] = dataset['interiorColor'].astype('category')
dataset['brandName'] = dataset['brandName'].astype('category')
dataset['modelName'] = dataset['modelName'].astype('category')
dataset['dealerID'] = dataset['dealerID'].astype('uint16')

print(dataset.info(memory_usage='deep'))


# events_by_color = (dataset['color'].value_counts()).head(5)
# top_colors = events_by_color.head(7)
# plt.figure(figsize=(10, 8))
# top_colors.plot(kind='bar', color='skyblue')
# plt.title('7 самых популярных цветов авто')
# plt.xlabel('Цвет')
# plt.ylabel('Число автомобилей')
# plt.xticks(rotation=45)
# plt.savefig('data/auto_data/plots/plot_1')

# # График 2. Скатерограмма  
# sns.scatterplot(data=dataset, x='isNew', y='askPrice')
# plt.title('Scatter plot of isNew vs askPrice') 
# plt.xlabel('isNew') 
# plt.ylabel('askPrice') 
# plt.xticks([0, 1], ['False', 'True'])
# plt.savefig('data/auto_data/plots/plot_2')

# # График 3. Построение тепловой карты для числовых столбцов
# numerical_df = dataset.select_dtypes(include=['uint32', 'uint16'])
# plt.figure(figsize=(10, 8))
# heatmap = sns.heatmap(numerical_df.corr(), annot=True, cmap='crest', fmt='.2f')
# plt.title('Correlation Heatmap')
# heatmap.get_figure().savefig("data/auto_data/plots/plot_3.png") 

# График 4. Круговая диаграмма
# value_counts = dataset['color'].value_counts()
# filtered_values = value_counts[value_counts >= 850].index.tolist()
# dataset['color'] = dataset['color'].apply(lambda x: x if x in filtered_values else 'Other')
# plt.figure(figsize=(8, 8))
# dataset['color'].value_counts().plot.pie(autopct='%1.1f%%', startangle=90, colors=sns.color_palette('pastel'))
# plt.title('Популярные цвета')
# plt.savefig('data/auto_data/plots/plot_4.png')

# График 5. Линейный
# plt.figure(figsize=(10, 6))
# plt.plot(dataset['askPrice'], dataset['msrp'])
# plt.xlabel('askPrice')
# plt.ylabel('MSRP')
# plt.title('Зависимость MSRP от askPrice')
# plt.xticks(rotation=45)
# plt.savefig('data/auto_data/plots/plot_5')



