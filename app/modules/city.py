import logging
from dadata import Dadata
from utils.settings import Settings
import requests
from typing import Union


class CityHelper:
    city_api = Dadata(Settings.get_city_api())
    geo_api = Settings.get_geocoder_api()
    GEO_URL = 'https://geocode-maps.yandex.ru/1.x/'

    @classmethod
    def get_city_coords(cls, city: str) -> Union[list[float], None]:
        """Retruns coordinates of place

        Args:
            city (str): name of place or city

        Returns:
            tuple: 
        """
        response = requests.get(cls.GEO_URL, params={
                                'apikey': cls.geo_api, 'geocode': city, 'format': 'json', 'results': 1})
        if response.status_code == 200:
            return [float(num) for num in response.json()['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos'].split(' ')]
        else:
            return None

    @classmethod
    def get_list_of_cities(cls, name: str) -> list[str]:
        try:
            return [city['value'] for city in cls.city_api.suggest("address", name)]
        except Exception as e:
            logging.warning(f"Can't find city by query {name}, error: {e}")
            return []
