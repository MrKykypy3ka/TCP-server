from analyser.analyser_map import *
from analyser.start_analyse import start
from socket_server import *
from API.yandex import *
from time import *
import datetime
import json
import threading

data = None
color_index = None

def load_data():
    global data
    global color_index
    with open('data/input/2022.json', encoding='utf-8') as file:
        data = json.load(file)
    with open('data/input/load_index.json') as file:
        color_index = json.load(file)


def check_coordination(current_time):
    date = datetime.datetime.strftime(datetime.date.today(), '%d.%m.%y')
    for area in data:
        if area != 'settings':
            for zone in data[area]:
                if zone != 'k':
                    for coor in data[area][zone]:
                        temp_coor = list(map(float, coor.split()))
                        get_map(longitude=temp_coor[0], latitude=temp_coor[1], map_parameters='trf', scale='3')
                        load_index = color_load()
                        with open('data/results/load.csv', 'a', encoding='utf=8') as file:
                            file.write(f'\n{area},{zone},{temp_coor[0]},{temp_coor[1]},{False},{date},{current_time},{color_index[load_index]}')


def check_time(current_time):
    for time_l in data['settings']['time']:
        if time_l == current_time:
            print(time_l, current_time)
            check_coordination(current_time)

def check_date(date):
    return True if date != datetime.datetime.now().date() else False

def analyse():
    d, m, y = map(int, data['settings']['date'][1].split('.'))
    date_end = (datetime.date(y, m, d) + datetime.timedelta(days=1)).strftime("%d.%m.%Y")
    while check_date(date_end):
        check_time(strftime("%H:%M", localtime()))
        sleep(60)


def main():
    server_thread = threading.Thread(target=start_server)
    server_thread.start()
    # start_server()
    # load_data()
    # analyse()
    # start()


if __name__ == "__main__":
    main()
