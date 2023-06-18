from working_with_data.data_cleaning import *
from working_with_data.modeling import *
from working_with_data.data_visualization import *
from working_with_data.report_generation import *
import pandas as pd
import os

def run_analysis(filename):
    pd.set_option('display.max_columns', None)
    pd.options.display.width = pd.options.display.max_columns = None
    df = pd.read_csv(f'data/results/{filename[:-5]}.csv')
    df['date'] = df['date'].apply(change_date)
    pivot_table_all_time, pivot_table_date, pivot_table_time = generate_pivot_table(df)
    table1 = result_all_time(pivot_table_all_time, filename).fillna(0).multiply(100).astype(int)
    table2 = result_date_and_time(pivot_table_date, filename).fillna(0).multiply(100).astype(int)
    table3 = result_date_and_time(pivot_table_time, filename).fillna(0).multiply(100).astype(int)
    max_result_red = ['white', 'green', 'yellow', 'red']
    max_result_yellow = ['white', 'green', 'yellow']

    custom_red = create_custom_colormap(max_result_red)
    custom_yellow = create_custom_colormap(max_result_yellow)

    image_path1 = f'data/results/all_time_{filename}.png'
    image_path2 = f'data/results/date_{filename}.png'
    image_path3 = f'data/results/time_{filename}.png'

    save_pivot_table_as_image(table1, image_path1, custom_yellow, 'Без учёта дат и времени', name_column='Объездной участок', fontsize=10, rotation=25)
    save_pivot_table_as_image(table2, image_path2, custom_red, 'С учётом дней недель', name_column='День недели')
    save_pivot_table_as_image(table3, image_path3, custom_red, 'С учётом времени', name_column='Время сбора данных', fontsize=8, rotation=25)

    pivot_table_all_time = pivot_table_all_time.fillna(0).multiply(100).astype(int)
    pivot_table_date = pivot_table_date.fillna(0).multiply(100).astype(int)
    pivot_table_time = pivot_table_time.fillna(0).multiply(100).astype(int)

    save_tables_and_images_to_word(pivot_table_all_time, table1, pivot_table_date, table2, pivot_table_time, table3, image_path1, image_path2, image_path3, f'data/results/Отчёт_{filename[:-5]}.docx')
    os.remove(image_path1)
    os.remove(image_path2)
    os.remove(image_path3)

