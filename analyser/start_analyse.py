import pandas as pd
from analyser.data_cleaning import change_date, change_time, generate_pivot_table
from analyser.modeling import result_date_and_time, result_all_time
from analyser.visualization import create_custom_colormap, save_pivot_table_as_image
from analyser.report_generation import save_tables_and_images_to_word
import os

def start():
    pd.set_option('display.max_columns', None)
    pd.options.display.width = pd.options.display.max_columns = None

    df = pd.read_csv("data/results/loaddd.csv")
    df['date'] = df['date'].apply(change_date)
    pivot_table_all_time, pivot_table_date, pivot_table_time = generate_pivot_table(df)
    table1 = result_all_time(pivot_table_all_time).fillna(0).multiply(100).astype(int)
    table2 = result_date_and_time(pivot_table_date).fillna(0).multiply(100).astype(int)
    table3 = result_date_and_time(pivot_table_time).fillna(0).multiply(100).astype(int)
    max_result_red = ['white', 'green', 'yellow', 'red']
    max_result_yellow = ['white', 'green', 'yellow']

    custom_red = create_custom_colormap(max_result_red)
    custom_yellow = create_custom_colormap(max_result_yellow)

    save_pivot_table_as_image(table1, 'data/results/all_time.png', custom_yellow, 'Без учёта дат и времени', name_column='Объездной участок', fontsize=10, rotation=25)
    save_pivot_table_as_image(table2, 'data/results/date.png', custom_red, 'С учётом дней недель', name_column='День недели')
    save_pivot_table_as_image(table3, 'data/results/time.png', custom_red, 'С учётом времени', name_column='Время сбора данных', fontsize=8, rotation=25)

    pivot_table_all_time = pivot_table_all_time.fillna(0).multiply(100).astype(int)
    pivot_table_date = pivot_table_date.fillna(0).multiply(100).astype(int)
    pivot_table_time = pivot_table_time.fillna(0).multiply(100).astype(int)

    save_tables_and_images_to_word(pivot_table_all_time, table1, pivot_table_date, table2, pivot_table_time, table3, 'data/results/all_time.png', 'data/results/date.png', 'data/results/time.png', 'data/results/Отчёт.docx')
    os.remove('data/results/all_time.png')
    os.remove('data/results/time.png')
    os.remove('data/results/date.png')