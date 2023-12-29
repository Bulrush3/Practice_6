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

need_types = read_types('data/game_data/dtypes.json') # не получилось использовать need_types как параметр dtype в методе read_csv
dataset = pd.read_csv("data/game_data/df.csv", usecols=lambda x: x in need_types.keys())
dataset['date'] = dataset['date'].astype('uint32')
dataset['number_of_game'] = dataset['number_of_game'].astype('uint8')
dataset['day_of_week'] = dataset['day_of_week'].astype('category')
dataset['park_id'] = dataset['park_id'].astype('category')
dataset['v_manager_name'] = dataset['v_manager_name'].astype('category')
dataset['length_minutes'] = dataset['length_minutes'].astype('float32')
dataset['v_hits'] = dataset['v_hits'].astype('float32')
dataset['h_hits'] = dataset['h_hits'].astype('float32')
dataset['h_walks'] = dataset['h_walks'].astype('float32')
dataset['h_errors'] = dataset['h_errors'].astype('float32')
print(dataset.info(memory_usage='deep'))

# (9)
    # Графики
# # # График 1. Столбчатая диаграмма
# plt.figure(figsize=(10,10))
# plot1 = dataset['day_of_week'].value_counts().plot(kind='bar', title='Частота игр по дням недели')
# plot1.figure.savefig("data/game_data/plots/plot1.png")

# # # График 2. Линейный
# dataset_copy = dataset.copy()
# dataset_copy['date'] = pd.to_datetime(dataset_copy['date'], unit='s')
# dataset_copy['year'] = dataset_copy['date'].dt.tz_localize('UTC')
# dataset_copy['day'] = dataset_copy['date'].dt.day
# gr_obj = dataset_copy.groupby('day')['length_minutes'].mean()
# plt.figure(figsize=(10, 6))
# plt.plot(gr_obj.index, gr_obj.values, color='green')
# plt.title('Games by duration and date of month')
# plt.xlabel('Day of the month')
# plt.ylabel('Average length of games')
# plt.xticks(range(6, 31))
# plt.grid(True)
# plt.savefig("data/game_data/plots/plot2.png")

# # График 3. Скатерограмма по признаку day_of_week 
# sns.scatterplot(data=dataset, x='day_of_week', y='length_minutes')
# plt.title('Scatter plot of day_of_week vs length_minutes') 
# plt.xlabel('day_of_week') 
# plt.ylabel('length_minutes') 
# plt.savefig("data/game_data/plots/plot3.png")

# # График 4. Построение тепловой карты для числовых столбцов
# numerical_df = dataset.select_dtypes(include=['uint32', 'uint8', 'float32'])
# plt.figure(figsize=(10, 8))
# heatmap = sns.heatmap(numerical_df.corr(), annot=True, cmap='coolwarm', fmt='.2f')
# plt.title('Correlation Heatmap')
# heatmap.get_figure().savefig("data/game_data/plots/plot4.png") 

# График 5. Круговая диаграмма
plt.figure(figsize=(8, 8))
dataset['day_of_week'].value_counts().plot.pie(autopct='%1.1f%%', startangle=90, colors=sns.color_palette('pastel'))
plt.title('Посещаемость по дням недели')
plt.savefig('data/game_data/plots/plot5.png')








