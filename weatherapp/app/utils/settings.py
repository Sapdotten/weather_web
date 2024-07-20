import os
from dotenv import load_dotenv


class Settings:
    """Class for getting consts and variables of env
    """
    load_dotenv()
    _CITY_API_KEY_NAME = 'CITY_API_KEY'
    _GEOCODER_API_NAME = 'GEOCODER_KEY'

    @classmethod
    def get_city_api(cls):
        return os.getenv(cls._CITY_API_KEY_NAME)

    @classmethod
    def get_geocoder_api(cls):
        return os.getenv(cls._GEOCODER_API_NAME)
