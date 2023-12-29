import pandas as pd 
import functions

pd.set_option("display.max_rows", 20, "display.max_columns", 60)

def read_file_zip(file_name):
    return next(pd.read_csv(file_name, chunksize=100000, compression='gzip'))

# (1)
    # Загружаем набор данных
file_name = "data/[4]vacancies.csv.gz"
dataset = read_file_zip(file_name)

# dataset.info(memory_usage='deep')

# (2, 3) 
    # Анализ набора данных по памяти, сортировка, запись в json
functions.get_file_size(dataset, file_name, "data/vacancies_data/file_size_unopt_res.json")

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

functions.get_file_size(dataset, file_name, "data/vacancies_data/file_size_opt_res.json")

# # (8) 
#     # Выбрать 10 колонок c преобразованием типов. Использование чанки

opt_dtypes = optimized_dataset.dtypes
need_column = {}
column_names = ["prof_classes_found", "employment_id", "schedule_name",
                "accept_kids", "address_city", "experience_name",  
                "salary_from", "salary_to", "area_id","employer_id",]

for key in column_names:
    need_column[key] = opt_dtypes[key]
    print(f"{key}:{opt_dtypes[key]}")
    
has_header = True
for chunk in pd.read_csv(file_name,
                        usecols=lambda x: x in column_names, 
                        dtype=need_column,
                        chunksize=100_000):
    print(functions.mem_usage(chunk))
    chunk.to_csv("data/vacancies_data/df.csv", mode="a", header=has_header)
    break

# with open("dtypes.json", mode="w") as file:
dtype_json = need_column.copy()
for key in dtype_json.keys():
    dtype_json[key] = str(dtype_json[key])
functions.write_to_json('data/vacancies_data/dtypes.json', dtype_json)