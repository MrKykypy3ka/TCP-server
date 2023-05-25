import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import math


def distribute_value_gaussian(value, k, mean=0, std=1):
    values = []
    while len(values) < k:
        sample = np.random.normal(mean, std)
        if sample > 0:
            values.append(sample)

    values = np.array(values)
    values = values / np.sum(values)  # Нормализация суммы значений до 1

    distributed_values = values * value
    return distributed_values.tolist()

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
        distributed_values = distribute_value_gaussian(pivot_table.loc[index, 'bad'], k)
        i = 0
        for column in table.columns:
            if table.loc[index, column] > 0:
                table.loc[index, column] += distributed_values[i]
                i += 1
    return table

def result_date(pivot_table):
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

def result_time(pivot_table):
    pass