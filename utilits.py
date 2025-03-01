import sys
from urllib3 import Retry
from requests.adapters import HTTPAdapter
import requests


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

def get_point(adress):
    server_address = "http://geocode-maps.yandex.ru/1.x/"
    geocoder_params = {
        "apikey": "8013b162-6b42-4997-9691-77b7074026e0",
        "format": "json",
        "geocode": adress}
    response = requests.get(server_address, params=geocoder_params)
    if not response:
        return None
    return response.json()['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']
