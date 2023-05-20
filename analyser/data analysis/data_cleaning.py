import pandas as pd
import datetime
from geopy.distance import geodesic




def change_time(time):
    h, m = map(int, time.split(':'))
    return h * 60 + m

def change_date(date):
    import datetime
    day, month, year = (int(x) for x in date.split('.'))
    ans = datetime.date(year, month, day)
    temp_date = ans.strftime("%A")
    if temp_date == 'Monday':
        return 1
    elif temp_date == 'Tuesday':
        return 2
    elif temp_date == 'Wednesday':
        return 3
    elif temp_date == 'Thursday':
        return 4
    elif temp_date == 'Friday':
        return 5
    elif temp_date == 'Saturday':
        return 6
    elif temp_date == 'Sunday':
        return 7




if __name__ == "__main__":
    pd.set_option('display.max_columns', None)

    df = pd.read_csv("data/output/load_ref.csv")
    df['date'] = df['date'].apply(change_date)
    df['time'] = df['time'].apply(change_time)


    df.to_csv('new.csv', index=False)
    group_all_time = df.groupby(['area', 'type_of_road'])['load_index'].mean()
    pivot_table_all_time = group_all_time.unstack()  # all_time

    group_date = df.groupby(['area', 'type_of_road', 'date'])['load_index'].mean()
    pivot_table_date = group_date.unstack()  # date

    group_time = df.groupby(['area', 'type_of_road', 'time'])['load_index'].mean()
    pivot_table_time = group_time.unstack()  # date
    table1 = result_all_time(pivot_table_all_time)
    table2 = result_date(pivot_table_date)
    print(table1.max().max())
    print(table2.max().max())

    colors_red = ['white', 'green', 'yellow', 'red']
    colors_yellow = ['white', 'green', 'yellow']

    custom_red = create_custom_colormap(colors_red)
    custom_yellow = create_custom_colormap(colors_yellow)


    save_pivot_table_as_image(table1, 'data/output/all_time.png', custom_yellow, 'Без учёта дат и времени')
    save_pivot_table_as_image(table2, 'data/output/time.png', custom_red, 'С учётом дней недель')
