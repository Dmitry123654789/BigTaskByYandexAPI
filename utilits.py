import math
import sys

import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry

def get_organisation_json(ll, organization):
    server_adress = 'https://search-maps.yandex.ru/v1'
    api_key = 'dda3ddba-c9ea-4ead-9010-f43fbc15c6e3'
    map_params = {
        'text': organization,
        "lang": "ru_RU",
        'apikey': api_key,
        "type": "biz",
        "results": 1,
        "ll": ll,
        "spn": '0.0005,0.0005'
    }
    session = requests.Session()
    retry = Retry(total=10, connect=5, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('https://', adapter)
    response = requests.get(server_adress, params=map_params)
    if not response:
        return []
    return response.json()["features"]

def get_response_map(ll, z, theme, *pt):
    server_address = "https://static-maps.yandex.ru/v1"
    apikey = '0eea7a3e-806e-4b45-8976-3c543752e89c'
    map_params = {
        'll': ll,
        'apikey': apikey,
        'z': z,
        'theme': theme,
        'pt': '~'.join([f'{x}' for x in list(*pt)]),
        'size': '600,380'
    }
    session = requests.Session()
    retry = Retry(total=10, connect=5, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('https://', adapter)
    response = requests.get(server_address, params=map_params)
    if not response:
        print(f"Ошибка выполнения запроса: {response.url}")
        sys.exit(1)
    return response.content


def get_json(adress):
    api_key = '8013b162-6b42-4997-9691-77b7074026e0'
    server_address = 'https://geocode-maps.yandex.ru/1.x/?'
    geocoder_request = f'{server_address}apikey={api_key}&geocode={adress}&format=json'
    response = requests.get(geocoder_request)
    if response:
        content = response.json()['response']['GeoObjectCollection']['featureMember']
        if len(content) == 0:
            return None
        return content[0]['GeoObject']
    else:
        return None


# Определяем функцию, считающую расстояние между двумя точками, заданными координатами
def lonlat_distance(a, b):
    degree_to_meters_factor = 111 * 1000  # 111 километров в метрах
    a_lon, a_lat = a
    b_lon, b_lat = b

    # Берем среднюю по широте точку и считаем коэффициент для нее.
    radians_lattitude = math.radians((a_lat + b_lat) / 2.)
    lat_lon_factor = math.cos(radians_lattitude)

    # Вычисляем смещения в метрах по вертикали и горизонтали.
    dx = abs(a_lon - b_lon) * degree_to_meters_factor * lat_lon_factor
    dy = abs(a_lat - b_lat) * degree_to_meters_factor

    # Вычисляем расстояние между точками.
    distance = math.sqrt(dx * dx + dy * dy)

    return distance
