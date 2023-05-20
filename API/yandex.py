import requests
import shutil
from PIL import Image, ImageDraw
import os


def get_map(longitude, latitude, map_parameters, scale, longitude_spn=0.005, latitude_spn=0.005, w=402, h=402):
    number = len(os.listdir('data/output/maps'))
    filename = f'data/output/maps/map{number+1}.png'
    link = f'https://static-maps.yandex.ru/1.x/' \
           f'?ll={longitude},{latitude}' \
           f'&size={w},{h}' \
           f'&spn={longitude_spn},{latitude_spn}' \
           f'&l={map_parameters}' \
           f'&scale={scale}' \
           f'&z={17}'
    question = requests.get(url=link, stream=True)
    with open(filename, 'wb') as out_file:
        shutil.copyfileobj(question.raw, out_file)


def draw_dot(name):
    image = Image.open(name)
    draw = ImageDraw.Draw(image)
    draw.line((325, 220, 325, 230), fill=(0, 0, 0), width=1)
    draw.line((320, 225, 330, 225), fill=(0, 0, 0), width=1)
    image.save(name)
