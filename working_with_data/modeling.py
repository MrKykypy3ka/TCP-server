import numpy as np
import json


def distribute_value_gaussian(value, k, mean=0, std=1):
    values = []
    while len(values) < k:
        sample = np.random.normal(mean, std)
        if sample > 0:
            values.append(sample)
    values = np.array(values)
    values = values / np.sum(values)
    distributed_values = values * value
    return distributed_values.tolist()


def load_user_koef(index, value, k):
    with open('data/input/2022.json', encoding='utf-8') as file:
        data = json.load(file)[index]['k']
    if len(data) == data.count(1):
        return 0
    for i in range(k):
        data[i] *= value
    return data

def count_not_nan(row):
    count = 0
    for elem in row:
        if elem > 0:
            count += 1
    return count

def result_all_time(pivot_table):
    table = pivot_table.drop('bad', axis=1)
    for index, row in table.iterrows():
        k = count_not_nan(row)
        distributed_values = load_user_koef(index, pivot_table.loc[index, 'bad'], k)
        if not distributed_values:
            distributed_values = distribute_value_gaussian(pivot_table.loc[index, 'bad'], k)
            distributed_values.sort(reverse=True)
        i = 0
        for column in table.columns:
            if table.loc[index, column] > 0:
                table.loc[index, column] += distributed_values[i]
                i += 1
    return table

def result_date_and_time(pivot_table):
    table = pivot_table.drop(index='bad', level='type_of_road')
    for column in table.columns:
        for area in table.index.get_level_values('area').unique():
            i = 0
            for road_type in table.index.get_level_values('type_of_road').unique():
                if (area, road_type) in table.index:
                    k = table.loc[area].shape[0]
                    distributed_values = distribute_value_gaussian(pivot_table.loc[(area, 'bad'), column], k)
                    if table.loc[(area, road_type), column] > 0:
                        table.loc[(area, road_type), column] += distributed_values[i]
                        i += 1
    return table