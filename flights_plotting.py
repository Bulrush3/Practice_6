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

need_types = read_types('data/flights_data/dtypes.json') # не получилось использовать need_types как параметр dtype в методе read_csv
dataset = pd.read_csv("data/flights_data/df.csv", usecols=lambda x: x in need_types.keys())
dataset['DAY'] = dataset['DAY'].astype('uint8')
dataset['FLIGHT_NUMBER'] = dataset['FLIGHT_NUMBER'].astype('uint16')
dataset['ORIGIN_AIRPORT'] = dataset['ORIGIN_AIRPORT'].astype('category')
dataset['SCHEDULED_DEPARTURE'] = dataset['SCHEDULED_DEPARTURE'].astype('uint16')
dataset['DEPARTURE_TIME'] = dataset['DEPARTURE_TIME'].astype('float32')
dataset['DEPARTURE_DELAY'] = dataset['DEPARTURE_DELAY'].astype('float32')
dataset['AIR_TIME'] = dataset['AIR_TIME'].astype('float32')
dataset['DISTANCE'] = dataset['DISTANCE'].astype('uint16')
dataset['WHEELS_ON'] = dataset['WHEELS_ON'].astype('float32')
dataset['SCHEDULED_ARRIVAL'] = dataset['SCHEDULED_ARRIVAL'].astype('uint16')

print(dataset.info(memory_usage='deep'))

# # График 1. 
# plt.figure(figsize=(10, 6))
# plt.plot(dataset['DAY'], dataset['DEPARTURE_DELAY'], marker='o', linestyle='-')
# plt.xlabel('Day')
# plt.ylabel('Departure Delay')
# plt.title('Задержка вылетов в зависимости от дня')
# plt.grid(True)
# plt.savefig('data/flights_data/plots/plot_1')

# # График 2.  
# plt.figure(figsize=(12, 6))
# monthly_flight_counts = dataset.groupby('DAY').size()
# monthly_flight_counts.plot(kind='bar', color='blue')
# plt.xlabel('День')
# plt.ylabel('Количество рейсов')
# plt.title('Количество рейсов по дням')
# plt.savefig('data/flights_data/plots/plot_2')

# # График 3.  
# plt.figure(figsize=(8, 6))
# sns.boxplot(y=dataset['AIR_TIME'])
# plt.ylabel('время в пути')
# plt.title('Boxplot времени в пути')
# plt.savefig('data/flights_data/plots/plot_3')

# # График 4.  
# plt.figure(figsize=(8, 6))
# sns.scatterplot(x='DISTANCE', y='AIR_TIME', data=dataset)
# plt.xlabel('DISTANCE')
# plt.ylabel('AIR_TIME')
# plt.title('Scatter Plot of DISTANCE vs AIR_TIME')
# plt.savefig('data/flights_data/plots/plot_4')

# # График 5.  
# numerical_df = dataset.select_dtypes(include=['uint32', 'uint16', 'uint8', 'float32'])
# plt.figure(figsize=(10, 8))
# heatmap = sns.heatmap(numerical_df.corr(), annot=True, cmap='crest', fmt='.2f')
# plt.title('Correlation Heatmap')
# heatmap.get_figure().savefig("data/flights_data/plots/plot_5.png") 



