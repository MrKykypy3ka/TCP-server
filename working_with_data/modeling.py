import math
import json

def distribute_value_gaussian(num_segments, k):
    mean = 0.5
    std_dev = 0.2
    total_sum = 0
    values = []
    for i in range(1, num_segments + 1):
        x = i / (num_segments + 1)
        exponent = -((x - mean) ** 2) / (2 * std_dev ** 2)
        value = (1 / (math.sqrt(2 * math.pi) * std_dev)) * math.exp(exponent)
        values.append(value)
        total_sum += value
    values = [value / total_sum for value in values]
    values.sort(reverse=True)
    for i, key in zip(range(len(k)), k):
        k[key] = values[i]
    return k

def result_all_time(pivot_table, filename):
    table = pivot_table.drop('bad', axis=1)
    for area, row in table.iterrows():
        with open(f'data/input/{filename}', encoding='utf-8') as file:
            k = json.load(file)[area]['k']
            num_segments = list(k.values()).count(0)
            if num_segments == len(k):
                k = distribute_value_gaussian(num_segments, k)
        for column in table.columns:
            if table.loc[area, column] > 0:
                print(pivot_table.loc[area, 'bad'], k[column])
                print(table.loc[area, column])
                table.loc[area, column] += pivot_table.loc[area, 'bad'] * k[column]
                print(table.loc[area, column])
                print()
    return table

def result_date_and_time(pivot_table, filename):
    table = pivot_table.drop(index='bad', level='type_of_road')
    for area, row in table.iterrows():
        with open(f'data/input/{filename}', encoding='utf-8') as file:
            k = json.load(file)[area[0]]['k']
            num_segments = list(k.values()).count(0)
            if num_segments == len(k):
                k = distribute_value_gaussian(num_segments, k)
        print(k)
        for column in table.columns:
            print(pivot_table.loc[(area[0], 'bad'), column])
            table.loc[area, column] += pivot_table.loc[(area[0], 'bad'), column] * k[area[1]]
    return table