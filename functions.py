import pandas as pd 
import numpy as np 
import json
import os

pd.set_option("display.max_rows", 20, "display.max_columns", 60)

def read_file(file_name, compression=None, chunksize=None, encoding=None):
    return pd.read_csv(file_name, compression=compression, chunksize=chunksize, encoding=encoding)

def get_file_size(dataset, file_name, output_file_name):
    result = dict()

    file_size = os.path.getsize(file_name)
    result["file_size"] = f"{file_size // 1024 ** 2} MB"
    result["in_memory_size"] = mem_usage(dataset)
    memory_stat = get_memory_stat_by_column(dataset)
    result["columns"] = memory_stat

    write_to_json(output_file_name, result)

def get_memory_stat_by_column(dataset):
    result = dict()
    # (2: a, b)
    memory_usage_stat = dataset.memory_usage(deep=True)
    total_memory_usage = memory_usage_stat.sum()
    print(f"file in memory size = {total_memory_usage // 1024} КБ")
    # (2: c)
    column_stat = list()
    for key in dataset.dtypes.keys():
        column_stat.append({
            "column_name": key,
            "memory_abs": memory_usage_stat[key] // 1024,
            "memory_per": round(memory_usage_stat[key] / total_memory_usage * 100, 4),
            "dtype": dataset.dtypes[key]
        })
        column_stat.sort(key=lambda x: x['memory_abs'], reverse=True)
        for column in column_stat:
            result[column["column_name"]] = dict()
            result[column["column_name"]]["memory_abs"] = f"{column['memory_abs']} KB"
            result[column["column_name"]]["memory_per"] = column['memory_per']
            result[column["column_name"]]["dtype"] = str(column['dtype'])

    return result

def mem_usage(pandas_obj):
    if isinstance(pandas_obj, pd.DataFrame):
        usage_b = pandas_obj.memory_usage(deep=True).sum()
    else:
        usage_b = pandas_obj.memory_usage(deep=True)
    usage_mb = usage_b / 1024 ** 2 
    return "{:03.2f} MB".format(usage_mb)

def opt_obj(df):
    converted_obj = pd.DataFrame()
    dataset_obj = df.select_dtypes(include=['object']).copy()

    for col in dataset_obj.columns:
        num_unique_values = len(dataset_obj[col].unique())
        num_total_values = len(dataset_obj[col])
        if num_unique_values / num_total_values < 0.5:
            converted_obj.loc[:, col] = dataset_obj[col].astype('category')
        else:
            converted_obj.loc[:, col] = dataset_obj[col]

    # print(mem_usage(dataset_obj))
    # print(mem_usage(converted_obj))
    return converted_obj

def opt_int(df):
    dataset_int = df.select_dtypes(include=['int'])
    converted_int = dataset_int.apply(pd.to_numeric, downcast='unsigned')
    # print(mem_usage(dataset_int))
    # print(mem_usage(converted_int))
    compare_ints = pd.concat([dataset_int.dtypes, converted_int.dtypes], axis=1)
    compare_ints.columns = ['before', 'after']
    compare_ints.apply(pd.Series.value_counts)
    # print(compare_ints)
    return converted_int

def opt_float(df):
    dataset_float = df.select_dtypes(include=['float'])
    converted_float = dataset_float.apply(pd.to_numeric, downcast='float')
    # print(mem_usage(dataset_float))
    # print(mem_usage(converted_float))
    compare_floats = pd.concat([dataset_float.dtypes, converted_float.dtypes], axis=1)
    compare_floats.columns = ['before', 'after']
    compare_floats.apply(pd.Series.value_counts)
    # print(compare_floats)
    return converted_float

def write_to_json(path, data):
    with open(path, 'w', encoding="utf-8") as f:
        f.write(json.dumps(data, ensure_ascii=False))