from socket_server import start
from analyser.analyser import *
from API.yandex import *
from time import *
import datetime
import json

data = dict()


def check_coordination(current_time):
    date = datetime.datetime.strftime(datetime.date.today(), '%d.%m.%y')
    for area in data:
        if area != 'settings':
            for zone in data[area]:
                for coor in data[area][zone]:
                    temp_coor = list(map(float, coor.split()))
                    get_map(longitude=temp_coor[0], latitude=temp_coor[1], map_parameters='trf', scale='1.3')
                    load_index = color_load()
                    with open('data/output/load.csv', 'a', encoding='utf=8') as file:
                        file.write(f'\n{area}, {zone}, {temp_coor[0]}, {temp_coor[1]}, {False}, {date}, {current_time}, {load_index}')


def check_time(current_time):
    global data
    with open('data/input/data.json') as file:
        data = json.load(file)
    # for time_l in data['settings']['time']:
        # if time == current_time:
        #     print(time_l)
    check_coordination(current_time)


def main():
    #  start()
    while True:
        check_time(strftime("%H:%M", localtime()))
        print("Complete")
        break
        # sleep(60)


if __name__ == "__main__":
    main()
