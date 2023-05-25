import pandas as pd
from analyser.data_cleaning import change_date, change_time, generate_pivot_table
from analyser.modeling import result_date, result_time, result_all_time
from analyser.visualization import create_custom_colormap, save_pivot_table_as_image
from analyser.report_generation import save_tables_and_images_to_word
import os


def start():
    pd.set_option('display.max_columns', None)
    pd.options.display.width = pd.options.display.max_columns = None

    df = pd.read_csv("data/results/load.csv")
    df['date'] = df['date'].apply(change_date)
    df['time'] = df['time'].apply(change_time)

    pivot_table_all_time, pivot_table_date, pivot_table_time = generate_pivot_table(df)
    table1 = result_all_time(pivot_table_all_time)
    table2 = result_date(pivot_table_date)

    max_result_red = ['white', 'green', 'yellow', 'red']
    max_result_yellow = ['white', 'green', 'yellow']

    custom_red = create_custom_colormap(max_result_red)
    custom_yellow = create_custom_colormap(max_result_red)

    save_pivot_table_as_image(table1, 'data/results/all_time.png', custom_yellow, 'Без учёта дат и времени')
    save_pivot_table_as_image(table2, 'data/results/time.png', custom_red, 'С учётом дней недель')

    save_tables_and_images_to_word(pivot_table_all_time, table1, pivot_table_date, table2, 'data/results/all_time.png', 'data/results/time.png', 'data/results/Отчёт.docx')
    os.remove('data/results/all_time.png')
    os.remove('data/results/time.png')