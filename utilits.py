import sys

import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry


def get_response_map(ll, z, theme, *pt):
    server_address = "https://static-maps.yandex.ru/v1"
    apikey = '0eea7a3e-806e-4b45-8976-3c543752e89c'
    map_params = {
        'll': ll,
        'apikey': apikey,
        'z': z,
        'theme': theme,
        'pt': '~'.join(list(*pt))
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
        content = response.json()['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']
        return content
    else:
        return None
