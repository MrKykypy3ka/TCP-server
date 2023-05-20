import pandas as pd
from analyser.data_cleaning import change_date, change_time, generate_pivot_table
from analyser.modeling import result_date, result_time, result_all_time
from analyser.visualization import create_custom_colormap, save_pivot_table_as_image


def start():
    pd.set_option('display.max_columns', None)

    df = pd.read_csv("data/output/load_ref.csv")
    df['date'] = df['date'].apply(change_date)
    df['time'] = df['time'].apply(change_time)

    pivot_table_all_time, pivot_table_date, pivot_table_time = generate_pivot_table(df)

    table1 = result_all_time(pivot_table_all_time)
    table2 = result_date(pivot_table_date)

    print(table1.max().max())
    print(table2.max().max())

    max_result_red = ['white', 'green', 'yellow', 'red']
    max_result_yellow = ['white', 'green', 'yellow']

    custom_red = create_custom_colormap(max_result_red)
    custom_yellow = create_custom_colormap(max_result_yellow)

    save_pivot_table_as_image(table1, 'data/output/all_time.png', custom_yellow, 'Без учёта дат и времени')
    save_pivot_table_as_image(table2, 'data/output/time.png', custom_red, 'С учётом дней недель')
