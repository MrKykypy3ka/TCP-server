import requests
import json
from PIL import Image, ImageDraw


def twoGis():
    link = 'https://routing.api.2gis.com/carrouting/6.0.0/global?key=1967db2b-de7d-46b3-b63a-ab040702a18a'
    headers = json.load(open("data/headers.json", "r"))
    data = open("data/data.json", "r").read()
    question = requests.post(url=link, headers=headers, data=data).text
    result = json.loads(question)
    with open('data/result.json', 'w', encoding='utf-8') as out_file:
        json.dump(result, out_file, separators=(', ', ': '), indent=4, ensure_ascii=False)


def get_city():
    link = f'https://catalog.api.2gis.com/3.0/items/geocode?' \
           f'lon={127.54388}&lat={50.25957}&fields=items.adm_div,items.address&type=street&key=ruhpjd9444'
    question = requests.get(url=link).text
    result = json.loads(question)
    with open('data/result.json', 'w', encoding='utf-8') as out_file:
        json.dump(result, out_file, separators=(', ', ': '), indent=4, ensure_ascii=False)



def coordination():
    link = f'https://catalog.api.2gis.com/2.0/region/search?q=Благовещенск&fields=items.bounds&key=ruhpjd9444'
    question = requests.get(url=link).text
    result = json.loads(question)
    with open('data/result.json', 'w', encoding='utf-8') as out_file:
        json.dump(result, out_file, separators=(', ', ': '), indent=4, ensure_ascii=False)


def draw_dot():
    image = Image.open('img.png')
    draw = ImageDraw.Draw(image)
    draw.line((325, 225, 325, 225), fill='red', width=1)
    image.save('img.png', quality=100)
