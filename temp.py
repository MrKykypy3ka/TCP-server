import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import datetime


def count_bad():
    df = pd.read_csv("data/output/load_ref.csv")
    temp = df['type_of_road'].value_counts()['bad']
    print(temp)

def work_df():
    def trafficlight(row):
        if row['type_of_road'] == 'crossroad':
            return 1
        return 0


    df = pd.read_csv("load.csv")
    df['trafficlight'] = df.apply(trafficlight, axis=1)
    df.to_csv('load.csv', index=False)

    print(df.head(50))


def date_time_second(date_time):
    print(date_time)
    date_format = '%Y-%m-%d %H:%M:%S'
    date_time = datetime.datetime.strptime(date_time, date_format)

    # Получение времени с начала эпохи в секундах
    return (date_time - datetime.datetime(1970, 1, 1)).total_seconds()


if __name__ == "__main__":
    count_bad()
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

    # Оценка производительности модели
    mae = mean_absolute_error(y_test, predicted_load)
    print('Средняя абсолютная ошибка:', mae)