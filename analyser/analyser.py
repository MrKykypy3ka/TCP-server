import math
from PIL import Image
import os
import cv2
import json


def color_load():
    number = len(os.listdir('data/output/maps'))
    name = f'data/output/maps/map{number}.png'
    im = Image.open(name).convert('RGB')
    center = im.getpixel((101, 101))
    # result = Image.new('RGB',color=center, size=im.size)
    # result.save(f'data/output/maps/color{number}.png')
    os.remove(name)
    return distance_color(center)


def distance_color(color_map):
    with open("data/input/color_road.json") as file:
        COLORS = json.load(file)
    for color in COLORS:
        COLORS[color] = list(map(int,COLORS[color].split()))

    distance = 442
    current_color = ""
    for color in COLORS:
        temp = math.sqrt((COLORS[color][0] - color_map[0]) ** 2 +
                         (COLORS[color][1] - color_map[1]) ** 2 +
                         (COLORS[color][2] - color_map[2]) ** 2)
        if temp < distance:
            distance = temp
            current_color = color
    return current_color


def trafficlight(im1, im2):
    needle = cv2.imread(im1)
    haystack = cv2.imread(im2)
    result = cv2.matchTemplate(needle, haystack, cv2.TM_CCOEFF_NORMED)
    minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(result)
    return True if maxVal > 0.6 else False


if __name__ == "__main__":
    # os.chdir(r'C:\Users\olegm\Documents\GitHub\road')
    os.chdir(r'C:\Users\Олег\PycharmProjects\road')
    with open("C:/Users/Олег/PycharmProjects/TCP-server/data/input/color_road.json") as file:
        COLORS = json.load(file)
    for color in COLORS:
        COLORS[color] = list(map(int,COLORS[color].split()))
    print(COLORS)

