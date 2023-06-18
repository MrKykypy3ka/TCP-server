from io import BytesIO
from PIL import Image
import requests


def get_map(longitude, latitude, map_parameters, scale, longitude_spn=0.005, latitude_spn=0.005, w=402, h=402):
    link = f'https://static-maps.yandex.ru/1.x/' \
           f'?ll={longitude},{latitude}' \
           f'&size={w},{h}' \
           f'&spn={longitude_spn},{latitude_spn}' \
           f'&l={map_parameters}' \
           f'&scale={scale}' \
           f'&z={17}'
    response = requests.get(url=link)
    return Image.open(BytesIO(response.content))
