from PIL import Image
import math
import cv2
import json
import os


def color_load(im):
    im2 = Image.open('data/input/white.png').convert('RGB')
    im2.paste(im, (0, 0), im)
    center = im2.getpixel((201, 201))
    return distance_color(center)


def distance_color(color_map):
    with open("data/input/color/color_road.json") as file:
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


def availability_trafficlight(im):
    im.save(f'data/results/maps/tf.png')
    bgr_image = cv2.cvtColor(cv2.imread(f'data/results/maps/tf.png'), cv2.COLOR_RGB2BGR)
    cascade = cv2.CascadeClassifier('traffic_light.xml')
    gray = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2GRAY)
    traffic_lights = cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(20, 20))
    os.remove(f'data/results/maps/tf.png')
    if len(traffic_lights) > 0:
        return 1
    else:
        return 0
