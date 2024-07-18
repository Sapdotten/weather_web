import os


class Settings:
    """Class for getting consts and variables of env
    """
    _CITY_API_KEY_NAME = 'CITY_API_KEY'

    @classmethod
    def get_city_api(cls):
        return os.getenv(cls._CITY_API_KEY_NAME)
