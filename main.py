from working_with_data.map_analysis import *
from working_with_data.data_analysis import *
from socket_server import *
from API.yandex import *
from time import *
import datetime
import json
import threading

data = None
color_index = None

def load_data(filename):
    global data
    global color_index
    with open(f'data/input/{filename}', encoding='utf-8') as file:
        data = json.load(file)
    with open('data/input/color/load_index.json') as file:
        color_index = json.load(file)

def check_coordination(current_time, filename):
    date = datetime.datetime.strftime(datetime.date.today(), '%d.%m.%y')
    for area in data:
        if area != 'settings':
            for zone in data[area]:
                if zone != 'k':
                    for coor in data[area][zone]:
                        temp_coor = list(map(float, coor.split()))
                        load_index = color_load(get_map(longitude=temp_coor[0],
                                                        latitude=temp_coor[1],
                                                        map_parameters='trf',
                                                        scale='3'))
                        trafficlight = availability_trafficlight(get_map(longitude=temp_coor[0],
                                                                         latitude=temp_coor[1],
                                                                         map_parameters='map',
                                                                         scale='3',
                                                                         longitude_spn=0.0002,
                                                                         latitude_spn=0.0002))
                        with open(f'data/results/{filename[:-5]}.csv', 'a', encoding='utf=8') as file:
                            file.write(f'\n{area},{zone},{temp_coor[0]},{temp_coor[1]},{trafficlight},{date},{current_time},{color_index[load_index]}')

def check_time(current_time, filename):
    for time_l in data['settings']['time']:
        if time_l == current_time:
            check_coordination(current_time, filename)

def checking_files():
    file_list = [file for file in os.listdir('data/input') if os.path.splitext(file)[1] == '.json']
    with open('queue.json', encoding='utf-8') as file:
        temp = json.load(file)
    for file in file_list:
        with open(f'data/input/{file}') as f1:
            data = json.load(f1)
            d, m, y = map(int, data['settings']['date'][0].split('.'))
            date_start = (datetime.date(y, m, d)).strftime("%d.%m.%Y")
            d, m, y = map(int, data['settings']['date'][1].split('.'))
            date_end = (datetime.date(y, m, d) + datetime.timedelta(days=1)).strftime("%d.%m.%Y")
            if date_start == datetime.datetime.now().date().strftime("%d.%m.%Y") and file not in temp['queue']:
                temp['queue'].append(file)
            if date_end <= datetime.datetime.now().date().strftime("%d.%m.%Y") and file in temp['queue']:
                temp['queue'].remove(file)
                run_analysis(file)
                print(f"Отчёт_{file[:-5]} Сформирован")
    with open(f'queue.json', "w", encoding='utf-8') as f2:
        json.dump(temp, f2, separators=(', ', ': '), indent=4, ensure_ascii=True)
    threading.Timer(10, checking_files).start()

def data_collection():
    with open('queue.json', encoding='utf-8') as file:
        file_list = json.load(file)['queue']
        for filename in file_list:
            load_data(filename)
            check_time(strftime("%H:%M", localtime()), filename)
    threading.Timer(60, data_collection).start()

def main():
    server_thread = threading.Thread(target=start_server)
    server_thread.start()

    checking_files_thread = threading.Thread(target=checking_files)
    checking_files_thread.start()

    data_collection_thread = threading.Thread(target=data_collection)
    data_collection_thread.start()

if __name__ == "__main__":
    main()
