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

need_types = read_types('data/vacancies_data/dtypes.json') # не получилось использовать need_types как параметр dtype в методе read_csv
dataset = pd.read_csv("data/vacancies_data/df.csv", usecols=lambda x: x in need_types.keys())
dataset['prof_classes_found'] = dataset['prof_classes_found'].astype('category')
dataset['employment_id'] = dataset['employment_id'].astype('category')
dataset['schedule_name'] = dataset['schedule_name'].astype('category')
dataset['accept_kids'] = dataset['accept_kids'].astype('bool')
dataset['address_city'] = dataset['address_city'].astype('category')
dataset['experience_name'] = dataset['experience_name'].astype('category')
dataset['salary_from'] = dataset['salary_from'].astype('float32')
dataset['salary_to'] = dataset['salary_to'].astype('float32')
dataset['area_id'] = dataset['area_id'].astype('uint16')
dataset['employer_id'] = dataset['employer_id'].astype('float32')

print(dataset.info(memory_usage='deep'))

# График 1
# plt.figure(figsize=(8, 6))
# sns.countplot(x='experience_name', data=dataset)
# plt.xlabel('Наличие опыта')
# plt.ylabel('Количество людей')
# plt.title('Количество людей по опыту')
# plt.savefig("data/vacancies_data/plots/plot1.png")

# График круговой диаграммы
# plt.figure(figsize=(8, 6))
# dataset['schedule_name'].value_counts().plot(kind='pie', autopct='%1.1f%%')
# plt.ylabel('')
# plt.title('Занятость людей')
# plt.savefig("data/vacancies_data/plots/plot2.png")

# Линейный график
# plt.figure(figsize=(8, 6))
# sns.lmplot(x='salary_from', y='salary_to', data=dataset)
# plt.xlabel('')
# plt.ylabel('')
# plt.title('')
# plt.savefig("data/vacancies_data/plots/plot3.png")

# 4. Линейный график для зарплаты в зависимости от опыта
# plt.figure(figsize=(12, 6))
# sns.lineplot(x='experience_name', y='salary_to', data=dataset, marker='o')
# plt.title('Зарплата в зависимости от опыта')
# plt.xlabel('Опыт')
# plt.ylabel('Зарплата (salary_from)')
# plt.savefig('data/vacancies_data/plots/plot4.png')

# 5. Корреляционная матрица для связи различных числовых переменных
# numerical_vars = ['salary_from', 'salary_to', 'area_id', 'employer_id']
# correlation_matrix = dataset[numerical_vars].corr()
# plt.figure(figsize=(8, 6))
# sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
# plt.title('Корреляционная матрица')
# plt.savefig('data/vacancies_data/plots/plot5.png')