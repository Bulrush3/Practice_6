import pandas as pd 
import functions

# source = 'https://www.kaggle.com/datasets/diegosilvadefrana/fisical-activity-dataset'

pd.set_option("display.max_rows", 20, "display.max_columns", 60)

def read_file_zip(file_name):
    return next(pd.read_csv(file_name, chunksize=100000, compression='zip'))

# (1)
    # Загружаем набор данных
file_name = "data/[6]physic.zip"
dataset = read_file_zip(file_name)

# dataset.info(memory_usage='deep')

# (2, 3) 
    # Анализ набора данных по памяти, сортировка, запись в json
functions.get_file_size(dataset, file_name, "data/physic_data/file_size_unopt_res.json")

# (4, 5, 6) 
    # Преобразования object в category с условием и понижающее преобразование колонок int и float
optimized_dataset = dataset.copy()
converted_obj = functions.opt_obj(dataset)
converted_int = functions.opt_int(dataset)
converted_float = functions.opt_float(dataset)

# # (7) 
#     # Повторный анализ набора данных со сравнением показателей занимаемой памяти
optimized_dataset[converted_obj.columns] = converted_obj
optimized_dataset[converted_int.columns] = converted_int
optimized_dataset[converted_float.columns] = converted_float

functions.get_file_size(dataset, file_name, "data/physic_data/file_size_opt_res.json")

# # (8) 
#     # Выбрать 10 колонок c преобразованием типов. Использование чанки

opt_dtypes = optimized_dataset.dtypes
need_column = {}
column_names = ["activityID", "heart_rate",
                'ankle magnetometer X', 'ankle magnetometer Y',
                'ankle magnetometer Z', "chest gyroscope X", 
                "chest gyroscope Y", "chest gyroscope Z"]

for key in column_names:
    need_column[key] = opt_dtypes[key]
    print(f"{key}:{opt_dtypes[key]}")
    
has_header = True
for chunk in pd.read_csv(file_name,
                        usecols=lambda x: x in column_names, 
                        dtype=need_column,
                        chunksize=100_000):
    print(functions.mem_usage(chunk))
    chunk.to_csv("data/physic_data/df.csv", mode="a", header=has_header)
    break

# with open("dtypes.json", mode="w") as file:
dtype_json = need_column.copy()
for key in dtype_json.keys():
    dtype_json[key] = str(dtype_json[key])
functions.write_to_json('data/physic_data/dtypes.json', dtype_json)