import math
from PIL import Image
import os
import cv2
import json


def color_load():
    filename = f'data/output/maps/map.png'
    im = Image.open(filename).convert('RGBA')
    im2 = Image.open('data/input/white.png').convert('RGB')
    im2.paste(im, (0, 0), im)
    center = im2.getpixel((201, 201))
    os.remove(filename)
    return distance_color(center)


def distance_color(color_map):
    with open("data/input/color_road.json") as file:
        COLORS = json.load(file)
    for color in COLORS:
        COLORS[color] = list(map(int, COLORS[color].split()))
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
    return 1 if maxVal > 0.6 else 0


if __name__ == "__main__":
    # os.chdir(r'C:\Users\olegm\Documents\GitHub\road')
    os.chdir(r'C:\Users\Олег\PycharmProjects\road')
    with open("C:/Users/Олег/PycharmProjects/TCP-server/data/input/color_road.json") as file:
        COLORS = json.load(file)
    for color in COLORS:
        COLORS[color] = list(map(int,COLORS[color].split()))
    print(COLORS)

