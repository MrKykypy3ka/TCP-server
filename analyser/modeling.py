import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense


def model():
    # Загрузка данных из CSV-файла
    data = pd.read_csv('data/output/load_ref.csv')

    # Преобразование столбцов 'date' и 'time' в формат datetime
    data['datetime'] = pd.to_datetime(data['date'] + ' ' + data['time'])

    # Вычисление количества секунд с начала эпохи (UNIX timestamp)
    data['timestamp'] = data['datetime'].apply(lambda x: int(x.timestamp()))
    data = data.drop(['date', 'time', 'datetime'], axis=1)
    # Выделение данных только для ремонтируемых участков
    repair_data = data[data['area'].isin(['Shevchenko', '50_Let_Oktbr', 'Amurskaya'])]

    # Создание нового столбца с целевой переменной
    repair_data['target_load'] = repair_data['load_index']

    # Преобразование категориальных признаков в числовые
    encoded_data = pd.get_dummies(repair_data, columns=['type_of_road', 'area'])

    print(data.info())
    # data['datetime'] = data['datetime'].apply(date_time_second)

    # Разделение данных на обучающий и тестовый наборы
    X = encoded_data.drop('target_load', axis=1)
    y = encoded_data['target_load']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # Создание и обучение модели случайного леса
    model = RandomForestRegressor(random_state=42)
    model.fit(X_train, y_train)

    # Предсказание нагрузки на объездных дорогах
    predicted_load = model.predict(X_test)
    print(len(predicted_load))


def result_all_time(pivot_table):
    table = pivot_table.drop('bad', axis=1)
    for index, row in table.iterrows():
        table.loc[index, 'road'] += pivot_table.loc[index, 'bad'] / 2
        table.loc[index, 'crossroad'] += pivot_table.loc[index, 'bad'] / 2
    return table

def result_date(pivot_table):
    table = pivot_table.drop(index='bad', level='type_of_road')
    for index, row in table.iterrows():
        for i in range(1, 3):
            table.loc[index[0], 'road'][i] += pivot_table.loc[index[0], 'bad'][i] / 2
            table.loc[index[0], 'crossroad'][i] += pivot_table.loc[index[0], 'bad'][i] / 2
    return table


def result_time(pivot_table):
    pass