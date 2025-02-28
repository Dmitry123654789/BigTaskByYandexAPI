import sys
from urllib3 import Retry
from requests.adapters import HTTPAdapter
import requests


def get_response_map(ll):
    server_address = "https://static-maps.yandex.ru/v1"
    apikey = '0eea7a3e-806e-4b45-8976-3c543752e89c'
    map_params = {
        'll': ll,
        'apikey': apikey
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
